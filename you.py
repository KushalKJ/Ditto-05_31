import glob
import os
import time
import pandas as pd
from openpyxl.utils.datetime import to_excel
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

import conf
from test import Emailer
import getpass
from tkinter import *
from tkinter import filedialog
import pandas as pd
from app import App
from configparser import ConfigParser


class App:
    def __init__(self, conf):
        self.conf = conf

    def run(self):
        print("running...")
        opts = Options()

        chrome_exe_path = self.conf.basic.get('CHROME_EXE_PATH')
        browser = Chrome(executable_path=chrome_exe_path, options=opts)
        browser.get("https://magnumpi-metrics-eu.aka.amazon.com/magnum/dl")
        browser.maximize_window()

        # time.sleep(5)

        username = browser.find_element_by_id("user_name")
        if self.conf.basic.get('VPN_UNAME'):
            username.send_keys(self.conf.basic.get('VPN_UNAME'))
        else:
            user_name = input("Enter user name : ")
            if not str(user_name.strip()):
                raise ValueError('Incorrect username entred!')
            username.send_keys(user_name)

        password = browser.find_element_by_id("password")
        if self.conf.basic.get('VPN_PWD'):
            password.send_keys(self.conf.basic.get('VPN_PWD'))
        else:
            password = getpass.getpass("Enter password : ")
            if not password:
                raise ValueError('No password entred!')
            password.send_keys(password)

        sign_in_button = browser.find_element_by_xpath("/html/body/main/section/div[1]/form/p[3]/input")
        sign_in_button.click()

        time.sleep(10)

        mag = browser.find_element_by_link_text("Download Search Results")
        mag.click()

        query_str = 'Duplicates_INPSI'
        queryname = browser.find_element_by_id("suggestions")
        queryname.send_keys(query_str)

        time.sleep(5)

        submit = browser.find_element_by_xpath("/html/body/div[1]/div[2]/div/form/button")
        submit.click()

        time.sleep(20)

        download = browser.find_element_by_xpath("/html/body/div/div[2]/div/p/a")
        download.click()

        time.sleep(30)

        browser.quit()

        list_of_files = glob.glob(self.conf.basic.get('FILE_INPUT_PATH'))
        latest_file = max(list_of_files, key=os.path.getctime)
        print(latest_file)

        path = latest_file

        df = pd.read_csv(latest_file)

        df_filterd = df[
            (df['status'] == 'UNASSIGNED') & (df['queue'] == 'COps') & (df['orderId'] != 'NULL') & (
                df['orderId'].notnull())]
        merged_df = pd.merge(df, df_filterd, how='inner', on=["asin", "orderId"])
        # (merged_df.head(50))
        order_ids = merged_df['orderId'][merged_df[
                                             'status_x'] == 'UNASSIGNED' 'ASSIGNED' 'CLOSED' 'CLOSED_ASIN_SUPPRESSED''PENDING_VENDORSELLER_COMMUNICATION''WORK_IN_PROGRESS' 'CLOSED_ASIN_REINSTATED'].to_numpy()
        # display(orderIds)
        fin_df = df_filterd[(df_filterd['orderId'].isin(order_ids))]
        print(fin_df.head(50))

        if not fin_df.empty:
            email_body = self.conf.basic.get('EMAIL_BODY')
            email = Emailer(subject=self.conf.basic.get('EMAIL_SUBJECT'),
                            recipient=self.conf.basic.get('EMAIL_LIST'),
                            text=email_body + fin_df.to_html()
                            )

            email.send_message()
            fin_df.to_csv(self.conf.basic.get('FILE_OUTPUT_PATH'), mode='a', index=False)
        else:
            raise ValueError('No Duplicates found!')


def import_Seller():
    global label_file
    global excel_filename
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select a file",
                                          filetype=(("Excel Files", "*.csv"),))
    label_file["text"] = filename
    file_path = label_file["text"]
    try:
        global excel_filename
        excel_filename = r"{}".format(file_path)
        global df
        df = pd.read_excel(excel_filename, engine='openpyxl')
    except ValueError:
        tk.messagebox.showinfo("Information", "The file you have chosen is invalid")
        return None
    except FileNotFoundError:
        tk.messagebox.showerror("Information", f"No such file as {file_path}")
        return None


root = Tk()
root.title("Ditto")
root.geometry("1000x500")
root.iconbitmap(r'C:\Users\kushakj\Downloads\ditto.ico')
root.configure(background='lightblue')

# mylabel = Label(root, text = "IN")
# mylabel.pack()

find_duplicates = Button(root, text="Find Duplicates", command=import_Seller)
find_duplicates.pack()

tool = Button(root, text="Run tool", command=run)
tool.pack()
root.mainloop()