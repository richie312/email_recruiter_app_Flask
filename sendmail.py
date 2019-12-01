# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 09:12:19 2019

@author: Richie
"""

# -*- coding: utf-8 -*-

import flask
from flask import Flask, request, json,render_template
import yagmail
import urllib.request
import mysql.connector
import mysql
import datetime
import os
host="richie-database.cml5lvgzqjbw.us-east-1.rds.amazonaws.com"
port=3306
dbname="RDS_MySql"
user="richie31"
password="Nirvikalpa!123"

connection = mysql.connector.connect(host=host, user=user,port=port,
                            passwd=password, db=dbname)
cursor = connection.cursor()    



app = Flask(__name__)
app.config['DEBUG'] = True

""" read the list of users"""
#with open('users.txt','r') as readfile:
#    email_list = readfile.readlines()

#email_list = [email_list[i].replace('\n',"") for i in range(len(email_list))]

@app.route("/")        # Standard Flask endpoint
def homepage():
    return render_template("user_form.html")

@app.route("/delete")        # Standard Flask endpoint
def delete():
    return render_template("delete_user.html")


@app.route('/addDetails', methods=['POST'])
def addDetails():
    data = request.form
    password = data['Password']
    main_dir = os.getcwd()
    yagmail.register("richie.chatterjee31@gmail.com", password)
    yag = yagmail.SMTP("richie.chatterjee31@gmail.com", password)
    html_msg = [yagmail.inline(main_dir + "\profile2.jpg"),
    main_dir+"\links.html",
    main_dir + "/Resume.pdf"]
    sql_query = "INSERT INTO company_email1 (Company_Name, Location, Email_Address, Application_Date)\
    VALUES (%s, %s, %s,%s)"
    Company = data['Company']
    Location = data['Location']
    email = data['Email Address']
    now = datetime.datetime.now()
    Applicaiton_Date = now.strftime('%Y-%m-%d %H:%M:%S')
    Subject_line = data['Subject']
    if Subject_line == "":
        default_subject = "Aritra_Chatterjee_Resume_DataScience_Python_Developer"
    else:
        default_subject = Subject_line
    val = (Company,Location,email,Applicaiton_Date)
    cursor.execute(sql_query,val)
    connection.commit()
    cursor.close()
    connection.close()
    """Send Email"""
    yag.send(email, default_subject, html_msg)    
    return render_template('user_form_response.html')

@app.route('/deleteuser', methods=['POST'])
def deleteuser():
    data = request.form
    with open('users.txt','r') as readfile:
        email_list = readfile.readlines()
    email_list = [email_list[i].replace('\n',"") for i in range(len(email_list))]
    email_list.remove(data['email_address'])    
    with open('users.txt','w') as outfile:
        outfile.write("\n".join(email_list))
    return render_template('user_form_response.html')
	
@app.route('/get_github_notification',methods = ['POST'])
def get_github_notification():    
    response = request.json
    with open('users.txt','r') as readfile:
        email_list = readfile.readlines()

    email_list = [email_list[i].replace('\n',"") for i in range(len(email_list))]

    with open('response.json','w') as outfile:
        json.dump(response, outfile)
    file_list = ['changes_required.html','response.json']
    for i in range(len(email_list)):
        mailto(email_list[i],file_list)
    return json.dumps(request.json)

if __name__ == '__main__':
    app.run(host = '0.0.0.0',debug=True,port=5001)
