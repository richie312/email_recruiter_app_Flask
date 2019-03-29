import yagmail
import urllib.request
import os
import pandas as pd
import csv
import glob
import mysql.connector
import mysql
os.chdir(r"C:\Users\Richie\Desktop\Email_Python")

connection = mysql.connector.connect(host='localhost',
                             database='mysql',
                             user='root',
                             password='')
cursor = connection.cursor()
print("Please enter your password")
password = str(input())

yagmail.register("richie.chatterjee31@gmail.com", password)
yag = yagmail.SMTP("richie.chatterjee31@gmail.com", password)

html_msg = [yagmail.inline(r"C:\Users\Richie\Desktop\Email_Python\profile.JPG"),
r"C:\Users\Richie\Desktop\Email_Python\links.html",
"C:/Users/Richie/Desktop/Email_Python/Resume.pdf"]



sql_query = "INSERT INTO job_mail_list (id, company_name, location, email)\
    VALUES (%s, %s,%s,%s)"
sql_query_lastRow = "SELECT MAX(id) FROM job_mail_list"
cursor.execute(sql_query_lastRow)
ID = cursor.fetchall()
print("Please enter the Company's/Consultant Name")
Company = input()
print("Please enter the Location Name")
Location = input()
print("Please enter the sender's email address")
email = input()

val = (ID[0][0]+1,Company,Location,email)

cursor.execute(sql_query,val)

connection.commit()

print(cursor.rowcount, "record inserted.")


# =============================================================================
# """Collect data """
# 
# 
# Last_Count = len(glob.glob1(r"C:\Users\Richie\Desktop\Email_Python",
#                             "*.csv"))
# 
# 
# dataframe = pd.read_csv("data_as_on{}.csv".format(Last_Count))
# 
# 
# print("Please enter the Company's/Consultant Name")
# Company = input()
# print("Please enter the Location Name")
# Location = input()
# print("Please enter the sender's email address")
# email = input()
# 
# """Apend the data inot existing one"""
# df2 = pd.DataFrame({'Location': Location, 'Company':Company,
#                     'Email':email},index=[0])
# Frame = dataframe.append(df2,ignore_index = True)
# """writing the data in new file"""
# Frame.to_csv("data_as_on{}.csv".format(len(Frame)))
# 
# 
# =============================================================================
"""Send Email"""

yag.send(email, "Aritra_Chatterjee_Resume_DataScience", html_msg)



