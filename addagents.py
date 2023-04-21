#addagents.py

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

def addAgents():    
    
    try:
        
        conn = pymysql.connect(user="root", password="", host="localhost", database="sunville")
        cur = conn.cursor()
        
        cur.execute("""insert into agents(AGENT_CODE ,AGENT_NAME,WORKING_AREA, COMMISSION,PHONE_NO,COUNTRY) values(%s,%s,%s,%s,%s,%s)""" ,
                    (agent_code.get(),agent_name.get(),working_area.get(),commission.get(),phone_no.get(),country.get()))
        conn.close()
        
        messagebox.showinfo("Save" , "Success!")
        b1['state']= 'enabled'
       
        agent_nameEntry.config(state='disabled')
        working_areaEntry.config(state='disabled')
        commissionEntry.config(state='disabled')
        phone_noEntry.config(state='disabled')
        countryEntry.config(state='disabled')
    except Exception as e:
        print(e)
       
        messagebox.showerror("Save" ,"Failed to save!")
        
def cancel():
    agent_code.set("")
    agent_name.set("")
    working_area.set("")  
    commission.set("")
    phone_no.set("")
    country.set("")
    root.destroy()


def validate(event , input):
    if( input == "Agent Code"):
        agentcode = agent_code.get()
        if (len(agentcode) == 4 and agentcode.isalnum()==True):
            agent_nameEntry.focus_set()
            agent_nameEntry.config(state='normal')
        else:
            messagebox.showerror("Invalid!" ,"Agent code has to be alphanumeric with length 4.")
            agent_codeEntry.focus_set()
    elif(input == "Agent Name"):
        if (agent_name.get().isalpha()==True and len(agent_name.get())>1):
            working_areaEntry.focus_set()
            working_areaEntry.config(state='normal')
        else:
            messagebox.showerror("Invalid!" ,"Agent Name has to be longer than 1 letter.")
            agent_nameEntry.focus_set()
    elif(input == "Working Area"):
        if (working_area.get().isalpha()==True and len(working_area.get())>1 ):
            commissionEntry.focus_set()
            commissionEntry.config(state='normal')
        else:
            messagebox.showerror("Invalid!" ,"Working Area has to be longer than 1 letter.")
            working_areaEntry.focus_set()
    elif( input == "Commission"):
        if (commission.get().replace('.', '', 1).isdigit()==True):  
            phone_noEntry.focus_set()
            phone_noEntry.config(state='normal')
        else:
            messagebox.showerror("Invalid!" ,"Commission has to be in decimal format (e.g., 0.11 for 11%).")
            commissionEntry.focus_set()
    elif( input == "Phone Number"):
        phn = phone_no.get().replace('-', '', 1)
        if (len(phn) == 11 and phn.isdigit()==True): 
            countryEntry.focus_set()
            countryEntry.config(state='normal')
        else:
            messagebox.showerror("Invalid!" ,"Phone Number has to be 11 digits long.")
            phone_noEntry.focus_set()  
    elif( input == "Country"):
        if len(country.get()) > -1 and country.get().isalpha()==True:
            pass
        else:
            messagebox.showerror("Invalid!" ,"Country has to be written using alphabets only.")
            countryEntry.focus_set()    

def readagents():
    readwindow = Tk()
    readwindow.title("Read Agent Data")
    readwindow.geometry('{}x{}'.format(800, 600))

    mainframe1 = Frame(readwindow)
    l = Label(readwindow, text='Here are the Results',font=('times', 20, 'bold'),background = '#154360',foreground = '#FDFEFE')
    l.place(x = 200, y = 10)

    df = pd.DataFrame() 
    df = TableModel.getSampleData()


    conn = pymysql.connect(user="root", password="", host="localhost", database="sunville")
    cur = conn.cursor()
        
    query = "select AGENT_CODE,AGENT_NAME,WORKING_AREA,PHONE_NO from agents"
    cur.execute(query)    
    df = pd.DataFrame(list(cur.fetchall()),columns =['AGENT_CODE','AGENT_NAME','WORKING_AREA','PHONE_NO'])
 

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
root.title("Agents")
root.geometry('{}x{}'.format(600, 500))
mainframe = Frame(root)
mainframe.pack()

agent_code = StringVar()
agent_name = StringVar()
working_area = StringVar()
commission = StringVar()
phone_no = StringVar()
country = StringVar()

agent_codeEntry = Entry(mainframe, width=20, textvariable=agent_code)
agent_codeEntry.grid(row=0, column=1 ,padx=5, pady=5)
agent_codeEntry.bind("<Return>", lambda event: validate(event, "Agent Code"))
agent_codeEntry.bind("<Tab>", lambda event: validate(event, "Agent Code"))

agent_nameEntry = Entry(mainframe, width=20, textvariable=agent_name)
agent_nameEntry.grid(row=1, column=1 ,padx=5, pady=5)
agent_nameEntry.bind("<Return>", lambda event: validate(event, "Agent Name"))
agent_nameEntry.bind("<Tab>", lambda event: validate(event, "Agent Name"))

working_areaEntry = Entry(mainframe, width=20, textvariable=working_area)
working_areaEntry.grid(row=2, column=1 ,padx=5, pady=5)
working_areaEntry.bind("<Return>", lambda event: validate(event, "Working Area"))
working_areaEntry.bind("<Tab>", lambda event: validate(event, "Working Area"))

commissionEntry = Entry(mainframe, width=20, textvariable=commission)
commissionEntry.grid(row=3, column=1 ,padx=5, pady=5)
commissionEntry.bind("<Return>", lambda event: validate(event, "Commission"))
commissionEntry.bind("<Tab>", lambda event: validate(event, "Commission"))

phone_noEntry = Entry(mainframe, width=20, textvariable=phone_no)
phone_noEntry.grid(row=4, column=1 ,padx=5, pady=5)
phone_noEntry.bind("<Return>", lambda event: validate(event, "Phone Number"))
phone_noEntry.bind("<Tab>", lambda event: validate(event, "Phone Number"))

countryEntry = Entry(mainframe, width=20, textvariable=country)
countryEntry.grid(row=5, column=1 ,padx=5, pady=5)
countryEntry.bind("<Return>", lambda event: validate(event, "Country"))
countryEntry.bind("<Tab>", lambda event: validate(event, "Country"))

agent_nameEntry.config(state='disabled')
working_areaEntry.config(state='disabled')
commissionEntry.config(state='disabled')
phone_noEntry.config(state='disabled')
countryEntry.config(state='disabled')

Label(mainframe, text='Agent Code:*', anchor='w').grid(row=0, column=0 ,padx=5, pady=5, sticky="w")
Label(mainframe, text='Agent Name:*', anchor='w').grid(row=1, column=0 ,padx=5, pady=5, sticky="w")
Label(mainframe, text='Working Area:*', anchor='w').grid(row=2, column=0 ,padx=5, pady=5, sticky="w")
Label(mainframe, text='Commission:*', anchor='w').grid(row=3, column=0 ,padx=5, pady=5, sticky="w")
Label(mainframe, text='Phone Number:*', anchor='w').grid(row=4, column=0 ,padx=5, pady=5, sticky="w")
Label(mainframe, text='Country:*', anchor='w').grid(row=5, column=0 ,padx=5, pady=5, sticky="w")
 
btnFrame = Frame(mainframe)
Button(btnFrame, text="Submit", command=addAgents).grid(row=0, column=1, padx=5, pady=5)
Button(btnFrame, text="Cancel", command=cancel).grid(row=0, column=2, padx=5, pady=5)
b1 = Button(btnFrame, text="Read Data",command=readagents)

b1.grid(row=0, column=3, padx=5, pady=5 )
btnFrame.grid(row=10, column=1, padx=5, pady=5)


root.mainloop()