#addorders.py

import tkinter
from tkinter import * 
from tkinter import messagebox
from functools import partial 
import sqlite3 
import pymysql
from venv import create
from tkinter.ttk import *
from tkcalendar import Calendar, DateEntry
import re
from datetime import datetime
import pandas as pd
from pandastable import Table, TableModel

# Saving student form data
def addOrders():    
    # Checking last input for validating , if not validated , shows error message
    if (len(ord_desc.get()) != 3 or ord_desc.get().isalpha()) == False:
        messagebox.showinfo("Save" , "Not Validated!")
        return
    
    try:
        # processing for three date variables : Birth Date , Start Date , End Date
        ordDateObj = datetime.strptime(ord_date.get(), '%d/%m/%Y')

        # Connecetion for mysql database
        conn = pymysql.connect(user="root", password="", host="localhost", database="sunville")
        cur = conn.cursor()
        # Excuting insert query 
        cur.execute("""insert into orders(ORD_NUM ,ORD_AMOUNT,ADVANCE_AMOUNT, ORD_DATE,CUST_CODE,AGENT_CODE,ORD_DESCRIPTION) values(%s,%s,%s,%s,%s,%s,%s)""" ,
                    (ord_num.get(),ord_amt.get(),adv_amt.get(),ordDateObj.strftime("%Y-%m-%d"),cust_code.get(),agent_code.get(),ord_desc.get()))
        conn.close()
        # Show message for successing
        messagebox.showinfo("Save" , "Success!")
        b1['state']= 'enabled'
        # Initializing for each input.
        ord_amtEntry.config(state='disabled')
        adv_amtEntry.config(state='disabled')
        cust_codeEntry.config(state='disabled')
        agent_codeEntry.config(state='disabled')
        ord_descEntry.config(state='disabled')
    except Exception as e:
        print(e)
        # If error on saving , shows error message.
        messagebox.showerror("Save" ,"Failed to save!")
# When clicking cancel button , application will be closed.
def cancel():
    ord_num.set("")
    ord_amt.set("")
    adv_amt.set("")  
    cust_code.set("")
    agent_code.set("")
    ord_desc.set("")
    root.destroy()

# Validating for each input
def validate(event , input):
    if( input == "Order Number"):
        ord_number = ord_num.get()
        if (len(ord_number) != 6 or ord_number.isdigit()==False):
            messagebox.showerror("Invalid!" ,"Order number has to be a 6 digit number.")
            ord_numEntry.focus_set()
        else:
            ord_amtEntry.focus_set()
            ord_amtEntry.config(state='normal')
    elif(input == "Order Amount"):
        if (ord_amt.get().isdigit()==True and float(ord_amt.get()) > 0 ):
            adv_amtEntry.focus_set()
            adv_amtEntry.config(state='normal')
        else:
            messagebox.showerror("Invalid!" ,"Order amount has to be a number greater than 0.")
            ord_amtEntry.focus_set()
    elif( input == "Advance Amount"):
        if (adv_amt.get().isdigit()==True and float(adv_amt.get()) >= 0 and float(adv_amt.get()) <=float(ord_amt.get()) ):
            cust_codeEntry.focus_set()
            cust_codeEntry.config(state='normal')
        else:
            messagebox.showerror("Invalid!" ,"Advance amount has to be a number greater than 0 and not greater than Order Amount.")
            adv_amtEntry.focus_set()
    elif( input == "Customer Code"):
        if (len(cust_code.get()) == 6 and cust_code.get().isalnum()==True):
            agent_codeEntry.focus_set()
            agent_codeEntry.config(state='normal')
        else:
            messagebox.showerror("Invalid!" ,"Customer code has to be alphanumberic with length 6.")
            cust_codeEntry.focus_set()
    elif( input == "Agent Code"):
        if (len(agent_code.get()) == 4 and agent_code.get().isalnum()==True):
            ord_descEntry.focus_set()
            ord_descEntry.config(state='normal')
        else:
            messagebox.showerror("Invalid!" ,"Agent code has to be alphanumberic with length 4.")
            agent_codeEntry.focus_set()  
    elif( input == "Order Description"):
        if len(ord_desc.get()) == 3 and ord_desc.get().isalpha():
            pass
        else:
            messagebox.showerror("Invalid!" ,"Order description has to be only three letters long.")
            ord_descEntry.focus_set()    

def readdata():
    readwindow = Tk()
    readwindow.title("Read Order Data")
    readwindow.geometry('{}x{}'.format(800, 600))
    
    mainframe1 = Frame(readwindow)
    l = Label(readwindow, text='Here are the Results',font=('times', 20, 'bold'),background = '#154360',foreground = '#FDFEFE')
    l.place(x = 200, y = 10)
    
    df = pd.DataFrame() 
    df = TableModel.getSampleData()
    
    
    conn = pymysql.connect(user="root", password="", host="localhost", database="sunville")
    cur = conn.cursor()
        # Excuting insert query 
    query = "select ORD_NUM,ORD_DATE,ORD_DESCRIPTION,CUST_CODE,AGENT_CODE from orders"
    cur.execute(query)    
    df = pd.DataFrame(list(cur.fetchall()),columns =['ORD_NUM','ORD_DATE','ORD_DESCRIPTION','CUST_CODE','AGENT_CODE'])
    #print (df)   
    
    table =Table(mainframe1, dataframe=df,showtoolbar=True, showstatusbar=True )
    table.currwidth = 700
    table.currheight = 500
    mainframe1.place(x = 200,y =200,anchor = "w")
    try:
        table.show()       
    except:
        pass
    conn.close()


# Creating main window and setting with width and height            
root = Tk()
root.title("Orders")
root.geometry('{}x{}'.format(600, 500))
mainframe = Frame(root)
mainframe.pack()

# Setting string variable for 6 input
ord_num = StringVar()
ord_amt = StringVar()
adv_amt = StringVar()
cust_code = StringVar()
agent_code = StringVar()
ord_desc = StringVar()
# Input for Order Number
ord_numEntry = Entry(mainframe, width=20, textvariable=ord_num)
ord_numEntry.grid(row=0, column=1 ,padx=5, pady=5)
ord_numEntry.bind("<Return>", lambda event: validate(event, "Order Number"))
ord_numEntry.bind("<Tab>", lambda event: validate(event, "Order Number"))
# Input for Order Amount
ord_amtEntry = Entry(mainframe, width=20, textvariable=ord_amt)
ord_amtEntry.grid(row=1, column=1 ,padx=5, pady=5)
ord_amtEntry.bind("<Return>", lambda event: validate(event, "Order Amount"))
ord_amtEntry.bind("<Tab>", lambda event: validate(event, "Order Amount"))
# Input for Advance Amount
adv_amtEntry = Entry(mainframe, width=20, textvariable=adv_amt)
adv_amtEntry.grid(row=2, column=1 ,padx=5, pady=5)
adv_amtEntry.bind("<Return>", lambda event: validate(event, "Advance Amount"))
adv_amtEntry.bind("<Tab>", lambda event: validate(event, "Advance Amount"))
# Input for Customer Code
cust_codeEntry = Entry(mainframe, width=20, textvariable=cust_code)
cust_codeEntry.grid(row=3, column=1 ,padx=5, pady=5)
cust_codeEntry.bind("<Return>", lambda event: validate(event, "Customer Code"))
cust_codeEntry.bind("<Tab>", lambda event: validate(event, "Customer Code"))
# Input for Agent Code
agent_codeEntry = Entry(mainframe, width=20, textvariable=agent_code)
agent_codeEntry.grid(row=4, column=1 ,padx=5, pady=5)
agent_codeEntry.bind("<Return>", lambda event: validate(event, "Agent Code"))
agent_codeEntry.bind("<Tab>", lambda event: validate(event, "Agent Code"))
# Input for Order Description
ord_descEntry = Entry(mainframe, width=20, textvariable=ord_desc)
ord_descEntry.grid(row=5, column=1 ,padx=5, pady=5)
ord_descEntry.bind("<Return>", lambda event: validate(event, "Order Description"))
ord_descEntry.bind("<Tab>", lambda event: validate(event, "Order Description"))

# First rest 5 inputs will be disabled for checking validation

ord_amtEntry.config(state='disabled')
adv_amtEntry.config(state='disabled')
cust_codeEntry.config(state='disabled')
agent_codeEntry.config(state='disabled')
ord_descEntry.config(state='disabled')

# Date picker for start date ,  end date
ord_date = StringVar()
DateEntry(mainframe , textvariable = ord_date , date_pattern='dd/mm/y' ).grid(row=7, column=1, padx=5, pady=5)

# Setting labels for each input
Label(mainframe, text='Order Number:*', anchor='w').grid(row=0, column=0 ,padx=5, pady=5, sticky="w")
Label(mainframe, text='Order Amount:*', anchor='w').grid(row=1, column=0 ,padx=5, pady=5, sticky="w")
Label(mainframe, text='Advance Amount:*', anchor='w').grid(row=2, column=0 ,padx=5, pady=5, sticky="w")
Label(mainframe, text='Customer Code:*', anchor='w').grid(row=3, column=0 ,padx=5, pady=5, sticky="w")
Label(mainframe, text='Agent Code:', anchor='w').grid(row=4, column=0 ,padx=5, pady=5, sticky="w")
Label(mainframe, text='Order Description:', anchor='w').grid(row=5, column=0 ,padx=5, pady=5, sticky="w")

Label(mainframe, text='Order Date:*', anchor='w').grid(row=7, column=0 ,padx=5, pady=5, sticky="w")

# Buttons for submit and cancel 
btnFrame = Frame(mainframe)
Button(btnFrame, text="Submit", command=addOrders).grid(row=0, column=1, padx=5, pady=5)
Button(btnFrame, text="Cancel", command=cancel).grid(row=0, column=2, padx=5, pady=5)
b1 = Button(btnFrame, text="Read Data",command= readdata )

b1.grid(row=0, column=3, padx=5, pady=5 )
btnFrame.grid(row=10, column=1, padx=5, pady=5)


root.mainloop()
