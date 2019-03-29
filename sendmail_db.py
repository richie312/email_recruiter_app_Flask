# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 10:37:20 2019
1
@author: Richie

Database Connector py file. This connects with database mysql and store data
into job_mail_list table.

"""

import mysql.connector
import mysql

connection = mysql.connector.connect(host='localhost',
                             database='mysql',
                             user='root',
                             password='')
cursor = connection.cursor()

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

cursor.execute(sql_query_lastRow)

val = (ID[0][0]+1,Company,Location,email)

cursor.execute(sql_query,val)

connection.commit()

print(cursor.rowcount, "record inserted.")
   
# =============================================================================
# """Magic function for looping all the values form excel and insert into db in one go"""
# val = []     
# for i in range(len(dataframe)):
#     val.append((i,dataframe.Company[i],dataframe.Location[i],
#                dataframe.Email[i]))
# 
# val = (ID,Company,Location,email)
# 
# for i in range(len(val)):
#     cursor.execute(sql_query, val[i])
# 
# =============================================================================

