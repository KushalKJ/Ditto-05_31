import glob
import os
import time
import pandas as pd
from openpyxl.utils.datetime import to_excel
from selenium.webdriver import Chrome, ChromeOptions
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from test import Emailer
import getpass
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging as log
import pandas


class App:
    def __init__(self, config):
        self.conf = config

    def run(self):
        log.info('Running app....')
        chrome_exe_path = self.conf.basic.get('CHROME_EXE_PATH')

        #browser = Chrome(executable_path=chrome_exe_path, options=opts)
        #browser.get("https://magnumpi-metrics-eu.aka.amazon.com/magnum/dl")
        #browser.maximize_window()

        options = ChromeOptions()
        # options.add_argument("headless")
        browser = Chrome(executable_path=chrome_exe_path, chrome_options=options)
        browser.get("https://magnumpi-metrics-eu.aka.amazon.com/magnum/dl")

        try:
            username = WebDriverWait(browser, 20).until(
                EC.presence_of_element_located((By.ID, "user_name"))
            )
            # username = browser.find_element_by_id("user_name")
            if self.conf.basic.get('VPN_UNAME'):
                username.send_keys(self.conf.basic.get('VPN_UNAME'))
                print("username.....")
            else:
                user_name = input("Enter user name : ")
                if not str(user_name.strip()):
                    raise ValueError('Incorrect username entered!')
                username.send_keys(user_name)
        except (NoSuchElementException, TimeoutException) as ex:
            log.info(f'Could not get username..{ex}')

        try:
            password = WebDriverWait(browser, 2).until(
                EC.presence_of_element_located((By.ID, "password"))
            )
            # password = browser.find_element_by_id("password")
            if self.conf.basic.get('VPN_PWD'):
                password.send_keys(self.conf.basic.get('VPN_PWD'))
                print("password.....")
            else:
                password = getpass.getpass("Enter password : ")
                if not password:
                    raise ValueError('No password entered!')
                password.send_keys(password)
        except (NoSuchElementException, TimeoutException) as ex:
            log.info(f'Could not get password..{ex}')

        try:
            sign_in_button = WebDriverWait(browser, 2).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/main/section/div[1]/form/p[3]/input"))
            )
            sign_in_button.click()
        except (NoSuchElementException, TimeoutException) as exc:
            log.info(f'Could not sign in..{exc}')

        """
        try:
            sign_in_button = browser.find_element_by_xpath("/html/body/main/section/div[1]/form/p[3]/input")
            sign_in_button.click()
        except NoSuchElementException as exc:
            log.info(f'')
        """

        try:
            # mag = browser.find_element_by_link_text("Download Search Results")
            mag = WebDriverWait(browser, 20).until(
                EC.presence_of_element_located((By.LINK_TEXT, "Download Search Results"))
            )
            mag.click()
        except (NoSuchElementException, TimeoutException) as exc:
            log.info(f'Could not find Download Search Results"..{exc}')
            print(f'exception in mag...{exc}')

        try:
            query_str = 'Duplicates_INPSI'
            # queryname = browser.find_element_by_id("suggestions")
            queryname = WebDriverWait(browser, 2).until(
                EC.presence_of_element_located((By.ID, "suggestions"))
            )
            queryname.send_keys(query_str)
        except (NoSuchElementException, TimeoutException) as exc:
            log.info(f'Could not find Download Search Results"..{exc}')
            print(f'exception suggestions...{exc}')

        try:
            # submit = browser.find_element_by_xpath("/html/body/div[1]/div[2]/div/form/button")
            submit = WebDriverWait(browser, 1).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div/form/button"))
            )
            submit.click()
        except (NoSuchElementException, TimeoutException) as exc:
            log.info(f'Could not find Download Search Results"..{exc}')
            print(f'exception in submit...{exc}')

        try:
            # download = browser.find_element_by_xpath("/html/body/div/div[2]/div/p/a")
            download = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div/div[2]/div/p/a"))
            )
            download.click()
        except (NoSuchElementException, TimeoutException) as exc:
            log.info(f'Could not find Download Search Results"..{exc}')
            print(f'exception in download...{exc}')

        time.sleep(5)
        browser.quit()

        list_of_files = glob.glob(self.conf.basic.get('FILE_INPUT_PATH'))
        path = max(list_of_files, key=os.path.getctime)
        latest_file = path  # r"{}".format(path)

        if os.path.exists(latest_file):
            print(" reading csv.... ", latest_file)
            # df = pd.read_csv(latest_file)
            # df = pandas.read_csv(filepath_or_buffer=latest_file)
            df = pd.read_csv(r'C:\Users\kushakj\Downloads\DuplicatesINPSI (2).csv')
            print("dataframe columns....", df.columns())
        else:
            raise FileNotFoundError(f'No file found at {latest_file}')

        df_filterd = df[
            (df['status'] == 'UNASSIGNED') & (df['queue'] == 'COps') & (df['orderId'] != 'NULL') & (
                df['orderId'].notnull())]
        merged_df = pd.merge(df, df_filterd, how='inner', on=["asin", "orderId"])
        # (merged_df.head(50))
        order_ids = merged_df['orderId'][merged_df['status_x'] != 'UNASSIGNED'].to_numpy()
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

