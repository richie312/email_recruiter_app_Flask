#Todo API Implementation using GraphQL
import datetime
from config.database import db_connection
from abc import abstractmethod
from flask import jsonify


def get_data():
    # todo return data/ Write in such a way that it can query like graphql
    connection = db_connection()
    cursor = connection.cursor()
    query = "select * from company_email1"
    cursor.execute(query)
    data = cursor.fetchall()
    # get the columns
    connection = db_connection()
    cursor = connection.cursor()
    col_query = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME=%s"
    cursor.execute(col_query,("company_email1",))
    cols = cursor.fetchall()
    dict_ = {"col": cols,"data": data}
    cursor.close()
    connection.close()
    return dict_

class Application(object):

    def __init__(self, bundle):
        self.company = bundle['Company']
        self.location = bundle['Location']
        self.email = bundle['Email Address']
        self.default_subject = "Aritra_Chatterjee_Resume_DataScience_Python_Developer"
        self.subject = bundle["Subject"] if bundle["Subject"] else self.default_subject
        self.application_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.connection = db_connection()
        self.cursor = self.connection.cursor()

    def add_details(self):
        sql_query = "INSERT INTO company_email1 (Company_Name, Location, Email_Address, Application_Date)\
        VALUES (%s, %s, %s,%s)"
        val = (self.company, self.location, self.email, self.application_date)
        self.cursor.execute(sql_query, val)
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

    @abstractmethod
    def get_data(self):
        #todo return data/ Write in such a way that it can query like graphql
        query = "select * from company_email1"
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        self.cursor.close()
        self.connection.close()
        return data

    def update(self):
        # pass sql to update table
        pass

    @abstractmethod
    def delete(company_name):
        query = ("""delete from company_email1 where Company_Name=%s;""", (company_name,))

