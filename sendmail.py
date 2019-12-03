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
import sys
host="richie-database.cml5lvgzqjbw.us-east-1.rds.amazonaws.com"
port=3306
dbname="RDS_MySql"
user="richie31"
password="Nirvikalpa!123"

app = Flask(__name__)
app.config['DEBUG'] = True

class BaseDataTables:
    
    def __init__(self, request, columns, collection):
        
        self.columns = columns

        self.collection = collection
         
        # values specified by the datatable for filtering, sorting, paging
        self.request_values = request.values
         
 
        # results from the db
        self.result_data = None
         
        # total in the table after filtering
        self.cardinality_filtered = 0
 
        # total in the table unfiltered
        self.cadinality = 0
 
        self.run_queries()
    
    def output_result(self):
        
        output = {}

        # output['sEcho'] = str(int(self.request_values['sEcho']))
        # output['iTotalRecords'] = str(self.cardinality)
        # output['iTotalDisplayRecords'] = str(self.cardinality_filtered)
        aaData_rows = []
        
        for row in self.result_data:
            aaData_row = []
            for i in range(len(self.columns)):
                print (row, self.columns, self.columns[i])
                aaData_row.append(str(row[ self.columns[i] ]).replace('"','\\"'))
            aaData_rows.append(aaData_row)
            
        output['aaData'] = aaData_rows
        
        return output
    
    def run_queries(self):
        
         self.result_data = self.collection
         self.cardinality_filtered = len(self.result_data)
         self.cardinality = len(self.result_data)

""" read the list of users"""
@app.route("/")        # Standard Flask endpoint
def homepage():
    return render_template("user_form.html")

@app.route("/delete")        # Standard Flask endpoint
def delete():
    return render_template("delete_user.html")


@app.route('/addDetails', methods=['POST'])
def addDetails():
    connection = mysql.connector.connect(host=host, user=user,port=port,
                            passwd=password, db=dbname)
    cursor = connection.cursor()    
    data = request.form
    passw = data['Password']
    main_dir = os.getcwd()
    yagmail.register("richie.chatterjee31@gmail.com", passw)
    yag = yagmail.SMTP("richie.chatterjee31@gmail.com", passw)
    html_msg = [yagmail.inline(os.path.join(main_dir,"profile2.jpg")),
    os.path.join(main_dir,"links.html"),
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

@app.route('/application_details', methods=['GET'])
def application_details():
    import requests
    response = requests.get("http://13.235.246.186/get_data")
    columns = response.json()['columns']
    return render_template('index.html', columns=columns)
    
@app.route('/_server_data')
def get_server_data():
    import requests
    response = requests.get("http://13.235.246.186/get_data")    
    columns = response.json()['columns']
    collection = [dict(zip(columns, response.json()['data'])) for i in range(len(response.json()['data']))]
    results = BaseDataTables(request, columns, collection).output_result()    
    return json.dumps(results)

if __name__ == '__main__':
    app.run(host = '0.0.0.0',debug=True,port=5001)
