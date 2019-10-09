# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 14:13:25 2019

@author: Richie
"""

from tkinter import *

root = Tk()

root.title("Welcome to the Email form")
root.configure(bg="white")

Label1 = Label(root,text = 'Enter the Company Name').grid(row = 1,column = 0, stick = W)
textentry1 = Entry(root,width = 20,bg="green")
textentry1.grid(row = 1,column=1)
Label2 = Label(root,text = 'Enter the Location').grid(row = 2,column = 0, stick = W)
textentry2 = Entry(root,width = 20,bg="green")
textentry2.grid(row = 2,column=1)
Label3 = Label(root,text = 'Enter email').grid(row = 3,column = 0, stick = W)
textentry3 = Entry(root,width = 20,bg="green")
textentry3.grid(row = 3,column=1)
Label4 = Label(root,text = 'Enter password').grid(row = 4,column = 0, stick = W)
textentry4 = Entry(root,width = 20,bg="green",show="*")
textentry4.grid(row = 4,column=1)
Label5 = Label(root,text = 'Subject Line').grid(row = 5,column = 0, stick = W)
textentry5 = Entry(root,width = 20,bg="green")
textentry5.grid(row = 5,column=1)



"""Define Function"""

def SendMail():
    import yagmail
    import urllib.request
    import mysql.connector
    import mysql
    import datetime
    host="richie-database.cml5lvgzqjbw.us-east-1.rds.amazonaws.com"
    port=3306
    dbname="RDS_MySql"
    user="richie31"
    password="Nirvikalpa!123"
    
    connection = mysql.connector.connect(host=host, user=user,port=port,
                               passwd=password, db=dbname)
    cursor = connection.cursor()
    
    password = textentry4.get()
    
    yagmail.register("richie.chatterjee31@gmail.com", password)
    yag = yagmail.SMTP("richie.chatterjee31@gmail.com", password)
    
    html_msg = [yagmail.inline(r"C:\Users\Richie\Desktop\Email_Python\profile2.jpg"),
    r"C:\Users\Richie\Desktop\Email_Python\links.html",
    "C:/Users/Richie/Desktop/Email_Python/Resume.pdf"]
    
    sql_query = "INSERT INTO company_email1 (Company_Name, Location, Email_Address, Application_Date)\
        VALUES (%s, %s, %s,%s)"
# =============================================================================
#     sql_query_lastRow = "SELECT MAX(id) FROM company_email1"
#     cursor.execute(sql_query_lastR
#     ID = cursor.fetchall()
#     
# =============================================================================
    Company = textentry1.get()
    
    Location = textentry2.get()
    
    email = textentry3.get()
    
    now = datetime.datetime.now()
    
    Applicaiton_Date = now.strftime('%Y-%m-%d %H:%M:%S')

    Subject_line = textentry5.get()
    
    if Subject_line == "":
        default_subject = "Aritra_Chatterjee_Resume_DataScience_Python_Developer"
    else:
        default_subject = Subject_line

    val = (Company,Location,email,Applicaiton_Date)
    
    cursor.execute(sql_query,val)
    
    connection.commit()
    
    output.insert("end","record/s successfully submitted to database ")
    
    """Send Email"""
    
    yag.send(email, default_subject, html_msg)
    output.insert("end","email has been sent to mentioned address.")
    connection.close()

theButton = Button(root,text = "Send Mail",bg = "white",fg="red",command = SendMail).grid(row = 6,column = 0)


"""Show the output"""

output = Text(root,width = 75,height = 6,wrap = WORD,background = "white")
output.grid(row = 7,column = 0, columnspan = 2)


root.mainloop()