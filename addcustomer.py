#addcustomer.py

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

def addCustomers():    

    if len(agent_code.get()) != 4 or agent_code.get().isalnum()==False:
        messagebox.showinfo("Save" , "Not Validated!")
        return
    try:
        conn = pymysql.connect(user="root", password="", host="localhost", database="sunville")
        cur = conn.cursor()
        cur.execute("""insert into customer(CUST_CODE ,CUST_NAME,CUST_CITY, WORKING_AREA,CUST_COUNTRY,GRADE,OPENING_AMT,RECEIVE_AMT,PAYMENT_AMT,OUTSTANDING_AMT,PHONE_NO,AGENT_CODE)
                    values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""" ,
                    (cust_code.get(),cust_name.get(),cust_city.get(),working_area.get(),cust_country.get(),grade.get(),opening_amt.get(),receive_amt.get(),payment_amt.get(),out_amt.get(),phone_no.get(),agent_code.get()))
        conn.close()
        messagebox.showinfo("Save" , "Success!")
        b1['state']= 'enabled'
        cust_nameEntry.config(state='disabled')
        cust_cityEntry.config(state='disabled')
        working_areaEntry.config(state='disabled')
        cust_countryEntry.config(state='disabled')
        gradeEntry.config(state='disabled')
        opening_amtEntry.config(state='disabled')
        receive_amtEntry.config(state='disabled')
        payment_amtEntry.config(state='disabled')
        out_amtEntry.config(state='disabled')
        phone_noEntry.config(state='disabled')
        agent_codeEntry.config(state='disabled')
        
    except Exception as e:
        print(e)
        
        messagebox.showerror("Save" ,"Failed to save!")

def cancel():
    cust_code.set("")
    cust_name.set("")
    cust_city.set("")  
    working_area.set("")
    cust_country.set("")
    grade.set("")
    opening_amt.set("")
    receive_amt.set("")  
    payment_amt.set("")
    out_amt.set("")
    phone_no.set("")
    agent_code.set("")
    root.destroy()

def validate(event , input):
    if( input == "Customer Code"):
        custcode = cust_code.get()
        if (len(custcode) == 6 and custcode.isalnum()==True):
            cust_nameEntry.focus_set()
            cust_nameEntry.config(state='normal')
        else:
            messagebox.showerror("Invalid!" ,"Customer code has to be alphanumeric with length 6.")
            cust_codeEntry.focus_set()
    elif(input == "Customer Name"):
        if (cust_name.get().isalpha()==True and len(cust_name.get())>0):
            cust_cityEntry.focus_set()
            cust_cityEntry.config(state='normal')
        else:
            messagebox.showerror("Invalid!" ,"Customer Name has to be atleast 1 letter.")
            cust_nameEntry.focus_set()
    elif(input == "Customer City"):
        if (cust_city.get().isalpha()==True and len(cust_city.get())>1 ):
            working_areaEntry.focus_set()
            working_areaEntry.config(state='normal')
        else:
            messagebox.showerror("Invalid!" ,"Customer city has to be longer than 1 letter.")
            cust_cityEntry.focus_set()
    elif( input == "Working Area"):
        if (len(working_area.get()) >0 and working_area.get().isalpha()==True):
            cust_countryEntry.focus_set()
            cust_countryEntry.config(state='normal')
        else:
            messagebox.showerror("Invalid!" ,"Working area has to be at least 1 letter.")
            working_areaEntry.focus_set()
    elif( input == "Customer Country"):
        if (len(cust_country.get()) >0 and cust_country.get().isalpha()==True):
            gradeEntry.focus_set()
            gradeEntry.config(state='normal')
        else:
            messagebox.showerror("Invalid!" ,"Customer Country has to be at least than 1 letter.")
            cust_countryEntry.focus_set()  
    elif( input == "Grade"):
        if grade.get().isdigit()==True:
            if (int(grade.get()) >=0 and int(grade.get())<=10):
                opening_amtEntry.focus_set()
                opening_amtEntry.config(state='normal')
            else:
                messagebox.showerror("Invalid!" ,"Grade should lie between 0-10.")
                gradeEntry.focus_set()    
        else:
            messagebox.showerror("Invalid!" ,"Grade should be numeric.")
            gradeEntry.focus_set()    
    elif( input == "Opening Amount"):
        if ((len(opening_amt.get()) >=2 and len(opening_amt.get())<=12) and opening_amt.get().isdigit()==True):
            receive_amtEntry.focus_set()
            receive_amtEntry.config(state='normal')
        else:
            messagebox.showerror("Invalid!" ,"Opening amount has to be numeric with length 2-12.")
            opening_amtEntry.focus_set()
    elif(input == "Receive Amount"):
        if ((len(receive_amt.get()) >=2 and len(receive_amt.get())<=12) and receive_amt.get().isdigit()==True):
            payment_amtEntry.focus_set()
            payment_amtEntry.config(state='normal')
        else:
            messagebox.showerror("Invalid!" ,"Receive amount has to be numeric with length 2-12.")
            receive_amtEntry.focus_set()
    elif(input == "Payment Amount"):
        if ((len(payment_amt.get()) >=2 and len(payment_amt.get())<=12) and payment_amt.get().isdigit()==True):
            out_amtEntry.focus_set()
            out_amtEntry.config(state='normal')
        else:
            messagebox.showerror("Invalid!" ,"Payment amount has to be numeric with length 2-12.")
            payment_amtEntry.focus_set()
    elif( input == "Outstanding Amount"):
        if ((len(out_amt.get()) >=2 and len(out_amt.get())<=12) and out_amt.get().isdigit()==True):
            phone_noEntry.focus_set()
            phone_noEntry.config(state='normal')
        else:
            messagebox.showerror("Invalid!" ,"Outstanding amount has to be numeric with length 2-12.")
            out_amtEntry.focus_set()
    elif( input == "Phone No"):
        phn = phone_no.get().replace('-', '', 1)
        if (len(phn) == 11 and phn.isdigit()==True): 
        
            agent_codeEntry.focus_set()
            agent_codeEntry.config(state='normal')
        else:
            messagebox.showerror("Invalid!" ,"Phone Number must be 11 digits.")
            phone_noEntry.focus_set() 
    elif( input == "Agent Code"):
        if (len(agent_code.get())==4 and agent_code.get().isalnum()==True):
            pass
        else:
            messagebox.showerror("Invalid!" ,"Agent Code must be alphanumeric with length 4.")
            agent_codeEntry.focus_set() 

def readcustomers():
    readwindow = Tk()
    readwindow.title("Read Customer Data")
    readwindow.geometry('{}x{}'.format(800, 600))

    mainframe1 = Frame(readwindow)
    l = Label(readwindow, text='Here are the Results',font=('times', 20, 'bold'),background = '#154360',foreground = '#FDFEFE')
    l.place(x = 200, y = 10)

    df = pd.DataFrame() 
    df = TableModel.getSampleData()


    conn = pymysql.connect(user="root", password="", host="localhost", database="sunville")
    cur = conn.cursor()
      
    query = "select CUST_CODE ,CUST_NAME,CUST_CITY, WORKING_AREA,CUST_COUNTRY,GRADE,OPENING_AMT,RECEIVE_AMT,PAYMENT_AMT,OUTSTANDING_AMT,PHONE_NO,AGENT_CODE from customer"
    cur.execute(query)    
    df = pd.DataFrame(list(cur.fetchall()),columns =['CUST_CODE' ,'CUST_NAME','CUST_CITY', 'WORKING_AREA','CUST_COUNTRY','GRADE','OPENING_AMT','RECEIVE_AMT','PAYMENT_AMT','OUTSTANDING_AMT','PHONE_NO','AGENT_CODE'])
   

    table =Table(mainframe1, dataframe=df,showtoolbar=True, showstatusbar=True )
    table.currwidth = 700
    table.currheight = 500
    mainframe1.place(x = 200,y =200,anchor = "w")
    try:
        table.show()       
    except:
        pass
    conn.close()

       
root = Tk()
root.title("Customers")
root.geometry('{}x{}'.format(600, 600))
mainframe = Frame(root)
mainframe.pack()

cust_name = StringVar()
cust_city = StringVar()
working_area = StringVar()
cust_country = StringVar()
grade = StringVar()
opening_amt = StringVar()
receive_amt = StringVar()
payment_amt = StringVar()
out_amt = StringVar()
phone_no = StringVar()
agent_code = StringVar()
cust_code = StringVar()
        
cust_codeEntry = Entry(mainframe, width=20, textvariable=cust_code)
cust_codeEntry.grid(row=0, column=1 ,padx=5, pady=5)
cust_codeEntry.bind("<Return>", lambda event: validate(event, "Customer Code"))
cust_codeEntry.bind("<Tab>", lambda event: validate(event, "Customer Code"))

cust_nameEntry = Entry(mainframe, width=20, textvariable=cust_name)
cust_nameEntry.grid(row=1, column=1 ,padx=5, pady=5)
cust_nameEntry.bind("<Return>", lambda event: validate(event, "Customer Name"))
cust_nameEntry.bind("<Tab>", lambda event: validate(event, "Customer Name"))

cust_cityEntry = Entry(mainframe, width=20, textvariable=cust_city)
cust_cityEntry.grid(row=2, column=1 ,padx=5, pady=5)
cust_cityEntry.bind("<Return>", lambda event: validate(event, "Customer City"))
cust_cityEntry.bind("<Tab>", lambda event: validate(event, "Customer City"))

working_areaEntry = Entry(mainframe, width=20, textvariable=working_area)
working_areaEntry.grid(row=3, column=1 ,padx=5, pady=5)
working_areaEntry.bind("<Return>", lambda event: validate(event, "Working Area"))
working_areaEntry.bind("<Tab>", lambda event: validate(event, "Working Area"))

cust_countryEntry = Entry(mainframe, width=20, textvariable=cust_country)
cust_countryEntry.grid(row=4, column=1 ,padx=5, pady=5)
cust_countryEntry.bind("<Return>", lambda event: validate(event, "Customer Country"))
cust_countryEntry.bind("<Tab>", lambda event: validate(event, "Customer Country"))

gradeEntry = Entry(mainframe, width=20, textvariable=grade)
gradeEntry.grid(row=5, column=1 ,padx=5, pady=5)
gradeEntry.bind("<Return>", lambda event: validate(event, "Grade"))
gradeEntry.bind("<Tab>", lambda event: validate(event, "Grade"))

opening_amtEntry = Entry(mainframe, width=20, textvariable=opening_amt)
opening_amtEntry.grid(row=6, column=1 ,padx=5, pady=5)
opening_amtEntry.bind("<Return>", lambda event: validate(event, "Opening Amount"))
opening_amtEntry.bind("<Tab>", lambda event: validate(event, "Opening Amount"))

receive_amtEntry = Entry(mainframe, width=20, textvariable=receive_amt)
receive_amtEntry.grid(row=7, column=1 ,padx=5, pady=5)
receive_amtEntry.bind("<Return>", lambda event: validate(event, "Receive Amount"))
receive_amtEntry.bind("<Tab>", lambda event: validate(event, "Receive Amount"))

payment_amtEntry = Entry(mainframe, width=20, textvariable=payment_amt)
payment_amtEntry.grid(row=8, column=1 ,padx=5, pady=5)
payment_amtEntry.bind("<Return>", lambda event: validate(event, "Payment Amount"))
payment_amtEntry.bind("<Tab>", lambda event: validate(event, "Payment Amount"))

out_amtEntry = Entry(mainframe, width=20, textvariable=out_amt)
out_amtEntry.grid(row=9, column=1 ,padx=5, pady=5)
out_amtEntry.bind("<Return>", lambda event: validate(event, "Outstanding Amount"))
out_amtEntry.bind("<Tab>", lambda event: validate(event, "Outstanding Amount"))

phone_noEntry = Entry(mainframe, width=20, textvariable=phone_no)
phone_noEntry.grid(row=10, column=1 ,padx=5, pady=5)
phone_noEntry.bind("<Return>", lambda event: validate(event, "Phone No"))
phone_noEntry.bind("<Tab>", lambda event: validate(event, "Phone No"))

agent_codeEntry = Entry(mainframe, width=20, textvariable=agent_code)
agent_codeEntry.grid(row=11, column=1 ,padx=5, pady=5)
agent_codeEntry.bind("<Return>", lambda event: validate(event, "Agent Code"))
agent_codeEntry.bind("<Tab>", lambda event: validate(event, "Agent Code"))


cust_nameEntry.config(state='disabled')
cust_cityEntry.config(state='disabled')
working_areaEntry.config(state='disabled')
cust_countryEntry.config(state='disabled')
gradeEntry.config(state='disabled')
opening_amtEntry.config(state='disabled')
receive_amtEntry.config(state='disabled')
payment_amtEntry.config(state='disabled')
out_amtEntry.config(state='disabled')
phone_noEntry.config(state='disabled')
agent_codeEntry.config(state='disabled')

Label(mainframe, text='Customer Code:*', anchor='w').grid(row=0, column=0 ,padx=5, pady=5, sticky="w")
Label(mainframe, text='Customer Name:*', anchor='w').grid(row=1, column=0 ,padx=5, pady=5, sticky="w")
Label(mainframe, text='Customer City:*', anchor='w').grid(row=2, column=0 ,padx=5, pady=5, sticky="w")
Label(mainframe, text='Working Area:*', anchor='w').grid(row=3, column=0 ,padx=5, pady=5, sticky="w")
Label(mainframe, text='Customer Country:*', anchor='w').grid(row=4, column=0 ,padx=5, pady=5, sticky="w")
Label(mainframe, text='Grade:*', anchor='w').grid(row=5, column=0 ,padx=5, pady=5, sticky="w")
Label(mainframe, text='Opening Amount:*', anchor='w').grid(row=6, column=0 ,padx=5, pady=5, sticky="w")
Label(mainframe, text='Receive Amount:*', anchor='w').grid(row=7, column=0 ,padx=5, pady=5, sticky="w")
Label(mainframe, text='Payment Amount:*', anchor='w').grid(row=8, column=0 ,padx=5, pady=5, sticky="w")
Label(mainframe, text='Outstanding Amount:*', anchor='w').grid(row=9, column=0 ,padx=5, pady=5, sticky="w")
Label(mainframe, text='Phone Number:*', anchor='w').grid(row=10,column=0 ,padx=5, pady=5, sticky="w")
Label(mainframe, text='Agent Code:*', anchor='w').grid(row=11,column=0 ,padx=5, pady=5, sticky="w")

btnFrame = Frame(mainframe)
Button(btnFrame, text="Submit", command=addCustomers).grid(row=15, column=1, padx=5, pady=5)
Button(btnFrame, text="Cancel", command=cancel).grid(row=15, column=2, padx=5, pady=5)
b1 = Button(btnFrame, text="Read Data",command=readcustomers)

b1.grid(row=15, column=3, padx=5, pady=5 )
btnFrame.grid(row=15, column=1, padx=5, pady=5)


root.mainloop()