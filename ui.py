# import tkinter as tk
#from tkinter import *
from tkinter import filedialog
from tkinter import ttk, Text, Button, LabelFrame, VERTICAL, E, NS, Scrollbar, Tk
import pandas as pd
from app import *
import conf
from __main__ import *

from configparser import ConfigParser

def import_Seller():
    global label_file
    global excel_filename
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select a file",
                                          filetype=(("CSV Files", "*.csv"),))

    file_path = filename
    try:
        global excel_filename
        excel_filename = r"{}".format(file_path)
        global df
        df = pd.read_csv(excel_filename)
    except ValueError:
        tk.messagebox.showinfo("Information", "The file you have chosen is invalid")
        return None
    except FileNotFoundError:
        tk.messagebox.showerror("Information", f"No such file as {file_path}")
        return None
    df_filterd = df[
    (df['status'] == 'UNASSIGNED') & (df['queue'] == 'COps') & (df['orderId'] != 'NULL') & (
    df['orderId'].notnull())]
    merged_df = pd.merge(df, df_filterd, how='inner', on=["asin", "orderId"])
   #(merged_df.head(50))
    order_ids = merged_df['orderId'][merged_df['status_x'] != 'UNASSIGNED'].to_numpy()
    # display(orderIds)
    fin_df = df_filterd[(df_filterd['orderId'].isin(order_ids))]
    print(fin_df.head(50))

def manual():
    os.system('python __main__.py')
    print("done")

#df_filterd = df[
#(df['status'] == 'UNASSIGNED') & (df['queue'] == 'COps') & (df['orderId'] != 'NULL') & (
#df['orderId'].notnull())]
#merged_df = pd.merge(df, df_filterd, how='inner', on=["asin", "orderId"])
#(merged_df.head(50))
#order_ids = merged_df['orderId'][merged_df['status_x'] == 'UNASSIGNED' 'ASSIGNED' 'CLOSED' 'CLOSED_ASIN_SUPPRESSED''PENDING_VENDORSELLER_COMMUNICATION''WORK_IN_PROGRESS' 'CLOSED_ASIN_REINSTATED'].to_numpy()
# display(orderIds)
    #fin_df = df_filterd[(df_filterd['orderId'].isin(order_ids))]
    #print(fin_df.head(50))

root = Tk()
root.title("Ditto")
root.geometry("1000x500")
root.iconbitmap(r'C:\Users\kushakj\Downloads\ditto.ico')
root.configure(background='lightblue')

# mylabel = Label(root, text = "IN")
# mylabel.pack()

find_duplicates = Button(root, text="Find Duplicates", command=import_Seller)
find_duplicates.pack()

tool = Button(root, text="Run tool", command = manual)
tool.pack()
root.mainloop()

