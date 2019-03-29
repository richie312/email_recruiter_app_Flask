# -*- coding: utf-8 -*-
"""
Created on Thu Jan 10 09:54:49 2019

@author: Richie
"""

import os
os.chdir(r"C:\Users\Richie\Desktop\Email_Python")
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import smtplib
from string import Template

# set up the SMTP server
s = smtplib.SMTP(host='smtp.gmail.com')
s.starttls()
s.login("richie.chatterjee31@gmail.com","Conciousness@123")

resume=open("Resume.html","r")
resume_read=resume.read()

msg = MIMEMultipart()
t=msg.attach(MIMEText(resume_read,'html'))

# to send
mailer = s
mailer.connect()
print("Enter the email address")
mailer.sendmail("richie.chatterjee31@gmail.com", input(), msg.as_string())
mailer.close()