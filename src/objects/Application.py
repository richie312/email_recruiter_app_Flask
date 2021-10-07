#Todo API Implementation using GraphQL
import datetime
from config.database import db_connection
from abc import abstractmethod
from flask import jsonify

class Application(object):

    def __init__(self, arg1=None,*bundle):
        # Check whether the instance is initiated with initializer or just using specific class method
        try:
            self.initializer = bundle[0]
        except IndexError:
            # return empty dictionary
            self.initializer = {}
        try:
            self.company = self.initializer['Company']
            self.location = self.initializer['Location']
            self.email = self.initializer['Email Address']
            self.default_subject = "Aritra_Chatterjee_Resume_DataScience_Python_Developer"
            self.subject = self.initializer["Subject"] if self.initializer["Subject"] else self.default_subject

        except KeyError:
            print("Application instance is initialized without initializer.")

        self.application_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.connection = db_connection()
        self.cursor = self.connection.cursor()

    def add_details(self):
        self.function = "add details"
        sql_query = "INSERT INTO company_email1 (Company_Name, Location, Email_Address, Application_Date)\
        VALUES (%s, %s, %s,%s)"
        val = (self.company, self.location, self.email, self.application_date)
        self.cursor.execute(sql_query, val)
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

    def update(self):
        self.function = "update"
        # pass sql to update table
        pass

    def delete(self,company_name):
        self.function = "delete"
        query = """delete from company_email1 where Company_Name=%s;"""
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

    def get_data(self):
        # todo return data/ Write in such a way that it can query like graphql
        query = "select * from company_email1"
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        # get the columns
        connection = db_connection()
        cursor = connection.cursor()
        col_query = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME=%s"
        cursor.execute(col_query, ("company_email1",))
        cols = cursor.fetchall()
        dict_ = {"col": cols, "data": data}
        cursor.close()
        connection.close()
        return dict_


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
    cursor.execute(col_query, ("company_email1",))
    cols = cursor.fetchall()
    dict_ = {"col": cols, "data": data}
    cursor.close()
    connection.close()
    return dict_
