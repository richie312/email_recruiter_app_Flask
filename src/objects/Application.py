from __future__ import annotations
import datetime
from config.database import Database
import pandas as pd


class Application(object):

    # initialising with all contact in order to maintain the local cache of contacts.
    # In this way cache can be updated to the database later rather than during sending email for a job.
    # it also helps in testing as well. Cache can be deleted.
    all_contacts: list["Application"] = []

    def __init__(self, bundle):
        # Check whether the instance is initiated with initializer or just using specific class method
        self.initializer = bundle
        try:
            self.company = self.initializer["Company"]
            self.location = self.initializer["Location"]
            self.email = self.initializer["Email Address"]
            self.default_subject = (
                "Aritra_Chatterjee_Resume_DataScience_Python_Developer"
            )
            self.subject = (
                self.initializer["Subject"]
                if self.initializer["Subject"]
                else self.default_subject
            )
            Application.all_contacts.append(self)

        except KeyError:
            print("Application instance is initialized without initializer.")

        self.application_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.conn_row_insertion_type = Database().row_insertion()
        self.cursor = self.conn_row_insertion_type.cursor()

    def add_details(self):
        self.function = "add details"
        sql_query = "INSERT INTO company_email1 (Company_Name, Location, Email_Address, Application_Date)\
        VALUES (%s, %s, %s,%s)"
        val = (self.company, self.location, self.email, self.application_date)
        self.cursor.execute(sql_query, val)
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

    @staticmethod
    def update(self):
        conn = Database().table_insertion().connect()
        df = pd.DataFrame()
        df["Location"] = [
            Application.all_contacts[i].location
            for i in range(len(Application.all_contacts))
        ]
        df["Application_Date"] = [
            Application.all_contacts[i].application_date
            for i in range(len(Application.all_contacts))
        ]
        df["Email_Address"] = [
            Application.all_contacts[i].email
            for i in range(len(Application.all_contacts))
        ]
        df["Company_Name"] = [
            Application.all_contacts[i].company
            for i in range(len(Application.all_contacts))
        ]
        print(df.head())
        df.to_sql(
            "company_email1",
            con=conn,
            schema="ContainerDatabase",
            if_exists="append",
            index=False,
        )
        print("Details added to the database. Closing the connection.")
        conn.close()

    def delete(self):
        query = """delete from company_email1 where Company_Name=%s;"""
        self.cursor.execute(query, (self.company,))
        self.conn_row_insertion_type.commit()
        self.cursor.close()
        self.conn_row_insertion_type.close()

    def get_data(self):
        # todo return data/ Write in such a way that it can query like graphql
        query = "select * from company_email1"
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        # get the columns
        connection = self.connection.row_insertion()
        cursor = connection.cursor()
        col_query = (
            "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME=%s"
        )
        cursor.execute(col_query, ("company_email1",))
        cols = cursor.fetchall()
        dict_ = {"col": cols, "data": data}
        cursor.close()
        connection.close()
        return dict_

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(" f"{self.initializer!r}" f")"


def get_data():
    # todo return data/ Write in such a way that it can query like graphql
    connection = Database().row_insertion()
    cursor = connection.cursor()
    query = "select * from company_email1"
    cursor.execute(query)
    data = cursor.fetchall()
    # get the columns
    connection = Database().row_insertion()
    cursor = connection.cursor()
    col_query = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME=%s"
    cursor.execute(col_query, ("company_email1",))
    cols = cursor.fetchall()
    dict_ = {"col": cols, "data": data}
    cursor.close()
    connection.close()
    return dict_
