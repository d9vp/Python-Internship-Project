#addcompany.py

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

def addCompanies():    

    if len(comp_city.get()) < 0 or comp_city.get().isalpha()==False:
        messagebox.showinfo("Save" , "Not Validated!")
        return
    try:
        conn = pymysql.connect(user="root", password="", host="localhost", database="sunville")
        cur = conn.cursor()
        
        cur.execute("""insert into company(COMPANY_ID, COMPANY_NAME,COMPANY_CITY) values(%s,%s,%s)""" ,
                    (comp_id.get(),comp_name.get(),comp_city.get()))
        conn.close()
        
        messagebox.showinfo("Save" , "Success!")
        b1['state']= 'enabled'
       
        comp_nameEntry.config(state='disabled')
        comp_cityEntry.config(state='disabled')

    except Exception as e:
        print(e)
        
        messagebox.showerror("Save" ,"Failed to save!")

def cancel():
    comp_id.set("")
    comp_name.set("")
    comp_city.set("")  
    root.destroy()

def validate(event , input):

    if( input == "Company ID"):
        compid = comp_id.get()
        if (len(compid) != 2 or compid.isdigit()==False):
            messagebox.showerror("Invalid!" ,"Company ID has to be numeric with length 2.")
            comp_idEntry.focus_set()
        else:
            comp_nameEntry.focus_set()
            comp_nameEntry.config(state='normal')
    elif(input == "Company Name"):
        if (comp_name.get().isdigit()==False and len(comp_name.get())>1):
            comp_cityEntry.focus_set()
            comp_cityEntry.config(state='normal')
        else:
            messagebox.showerror("Invalid!" ,"Company Name has to be longer that 1 character.")
            agent_nameEntry.focus_set()
    elif(input == "Company City"):
        if (comp_city.get().isalpha()==True and len(comp_city.get())>1 ):
            pass
        else:
            messagebox.showerror("Invalid!" ,"Company City has to be longer than 1 letter.")
            comp_cityEntry.focus_set()


def readcompanies():
    readwindow = Tk()
    readwindow.title("Read Company Data")
    readwindow.geometry('{}x{}'.format(800, 600))

    mainframe1 = Frame(readwindow)
    l = Label(readwindow, text='Here are the Results',font=('times', 20, 'bold'),background = '#154360',foreground = '#FDFEFE')
    l.place(x = 200, y = 10)

    df = pd.DataFrame() 
    df = TableModel.getSampleData()


    conn = pymysql.connect(user="root", password="", host="localhost", database="sunville")
    cur = conn.cursor()
       
    query = "select COMPANY_ID,COMPANY_NAME,COMPANY_CITY from company"
    cur.execute(query)    
    df = pd.DataFrame(list(cur.fetchall()),columns =['COMPANY_ID','COMPANY_NAME','COMPANY_CITY'])
   

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
root.title("Companies")
root.geometry('{}x{}'.format(600, 500))
mainframe = Frame(root)
mainframe.pack()

comp_id = StringVar()
comp_name = StringVar()
comp_city = StringVar()

comp_idEntry = Entry(mainframe, width=20, textvariable=comp_id)
comp_idEntry.grid(row=0, column=1 ,padx=5, pady=5)
comp_idEntry.bind("<Return>", lambda event: validate(event, "Company ID"))
comp_idEntry.bind("<Tab>", lambda event: validate(event, "Company ID"))

comp_nameEntry = Entry(mainframe, width=20, textvariable=comp_name)
comp_nameEntry.grid(row=1, column=1 ,padx=5, pady=5)
comp_nameEntry.bind("<Return>", lambda event: validate(event, "Company Name"))
comp_nameEntry.bind("<Tab>", lambda event: validate(event, "Company Name"))

comp_cityEntry = Entry(mainframe, width=20, textvariable=comp_city)
comp_cityEntry.grid(row=2, column=1 ,padx=5, pady=5)
comp_cityEntry.bind("<Return>", lambda event: validate(event, "Company City"))
comp_cityEntry.bind("<Tab>", lambda event: validate(event, "Company City"))

comp_nameEntry.config(state='disabled')
comp_cityEntry.config(state='disabled')

Label(mainframe, text='Company ID:*', anchor='w').grid(row=0, column=0 ,padx=5, pady=5, sticky="w")
Label(mainframe, text='Company Name:*', anchor='w').grid(row=1, column=0 ,padx=5, pady=5, sticky="w")
Label(mainframe, text='Company City:*', anchor='w').grid(row=2, column=0 ,padx=5, pady=5, sticky="w")


btnFrame = Frame(mainframe)
Button(btnFrame, text="Submit", command=addCompanies).grid(row=0, column=1, padx=5, pady=5)
Button(btnFrame, text="Cancel", command=cancel).grid(row=0, column=2, padx=5, pady=5)
b1 = Button(btnFrame, text="Read Data",command=readcompanies)

b1.grid(row=0, column=3, padx=5, pady=5 )
btnFrame.grid(row=10, column=1, padx=5, pady=5)


root.mainloop()