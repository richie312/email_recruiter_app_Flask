# -*- coding: utf-8 -*-

import flask
from flask import Flask, request, json,render_template,redirect,url_for,jsonify,json
import yagmail
import urllib.request
import mysql.connector
import mysql
import datetime
import os
import sys
from decrypt import *

with open(r'database_auth.json','r') as readfile:
    db_auth = json.load(readfile)

""" decrypt the database details"""
main_dir = os.getcwd()
os.listdir(os.path.join(main_dir,'auth'))

db_auth = {'dbname.txt':'key_dbname.txt',
           'db_pass.txt':'key_db_pass.txt',
           'host.txt':'key_host.txt',
           'dbuser.txt':'key_dbuser.txt'}
filename = {}
for i in db_auth.keys():
    with open(r'auth/' +i, 'r') as readfile:
        filename['{}'.format(i.split('.')[0])]= json.load(readfile)

file_key = {}
for i in db_auth.keys():
    with open(r'auth/' +db_auth[i], 'r') as readfile:
        file_key['{}'.format(db_auth[i].split('.')[0])]= json.load(readfile)

db_auth = {}
for i in filename.keys():
    db_auth[i] = decrypt(eval(filename[i]),eval(file_key['key_'+i])).decode("utf-8")

app = Flask(__name__)
app.config['DEBUG'] = True

""" read the list of users"""
@app.route("/")        # Standard Flask endpoint
def homepage():
    return render_template("user_form.html")

@app.route('/addDetails', methods=['POST'])
def addDetails():
    connection = mysql.connector.connect(host=db_auth['host'], 
                                         user=db_auth['dbuser'],
                                         port=3306,
                                         passwd=db_auth['db_pass'], 
                                         db=db_auth['dbname'])
    cursor = connection.cursor()
    data = request.form
    passw = data['Password']
    main_dir = os.getcwd()
    yagmail.register("richie.chatterjee31@gmail.com", passw)
    yag = yagmail.SMTP("richie.chatterjee31@gmail.com", passw)
    image_folder = os.path.join(main_dir,'images')
    template_folder = os.path.join(main_dir,'templates')
    html_msg = [yagmail.inline(os.path.join(image_folder,"profile2.jpg")),
    os.path.join(template_folder,"links.html"),
    main_dir + "/docs/Resume.pdf"]    
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

@app.route('/application_details', methods=['GET'])
def application_details():
    return render_template('application_table.html')

@app.route('/delete_form', methods=['GET'])
def delete_form():
    return render_template('delete_details.html')



@app.route('/delete', methods=['POST'])
def delete():
    templateData = {}
    connection = mysql.connector.connect(host=db_auth['host'], 
                                         user=db_auth['dbuser'],
                                         port=3306,
                                         passwd=db_auth['db_pass'], 
                                         db=db_auth['dbname'])

    cursor = connection.cursor()    
    data = request.form
    cursor.execute("""delete from company_email1 where Company_Name=%s;""",(data['Company'],))
    connection.commit()
    cursor.close()
    connection.close()    
    templateData['redirect_url'] = url_for('application_details')
    return render_template('delete_details_response.html',**templateData)

@app.route('/index_get_data')
def stuff():
    import requests
    response = requests.get("http://13.235.246.186/get_data")    
    columns = response.json()['columns']    
    collection = [dict(zip(columns, response.json()['data'][i])) for i in range(len(response.json()['data']))]
    data = {"data": collection}
    return jsonify(data)

if __name__ == '__main__':
    app.run(host = '0.0.0.0',debug=True,port=5001)
