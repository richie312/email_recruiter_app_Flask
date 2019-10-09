# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 08:43:32 2019

@author: aritra.chatterjee
"""

from tkinter import *
root = Tk()
root.title("Welcome to the Email form")
root.configure(bg="white")

Label1 = Label(root,text = 'paste the Company/Recruiter email addresses to which you want to send the followup email.').grid(row = 1,column = 0, stick = W)
textentry4 = Entry(root,width = 100,bg="green")
textentry4.grid(row = 1,column=1)

def fetch_Details():
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
    password = "Conciousness@123"
    sql_query = "select Email_Address from company_email1 where Location = 'Hyderabad' order by Application_Date Desc limit 10;"

    cursor.execute(sql_query)
    email_list = cursor.fetchall()
    email=[]
    for i in range(len(email_list)):
        email.extend(email_list[i])
    email_display=str(email)
    output.insert("end",email_display)
    connection.commit()
    return email
    
FetchButton = Button(root,text = "Fetch Details",bg = "white",fg="red",command = fetch_Details).grid(row = 4,column = 0)

    
def SendMail():
    import yagmail
    password='Conciousness@123'
    yagmail.register("richie.chatterjee31@gmail.com", password)
    yag = yagmail.SMTP("richie.chatterjee31@gmail.com", password)
    
    html_msg = [yagmail.inline(r"C:\Users\aritra.chatterjee\Desktop\Email_Python\profile2.jpg"),
    r"C:\Users\aritra.chatterjee\Desktop\Email_Python\links.html",
    "C:/Users/aritra.chatterjee/Desktop/Email_Python/Resume.pdf"]
    emails = textentry4.get()
    list_emails=emails.split(',')
    """Send Email"""
    for i in range(len(list_emails)):
        yag.send(list_emails[i], "Aritra_Chatterjee_Resume_DataScience", html_msg)
        output.insert('end','Congrats! Mail has been sent to above edited list of recipients.')
        
Label2 = Label(root,text = 'The last 10 Company/Recruiter email addresses').grid(row = 3,column = 0, stick = W)
output = Text(root,width = 75,height = 6,wrap = WORD,background = "white")
output.grid(row = 4,column = 1, columnspan = 2)
SendButton = Button(root,text = "Send Mail",bg = "white",fg="red",command = SendMail).grid(row = 5,column = 0)
output = Text(root,width = 75,height = 6,wrap = WORD,background = "white")
output.grid(row = 5,column = 1, columnspan = 2)


root.mainloop()