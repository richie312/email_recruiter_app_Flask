import os
import json
import mysql.connector
from src.src_context import root_dir
from dotenv import load_dotenv
from sqlalchemy import create_engine
""" decrypt the database details"""
load_dotenv(os.path.join(root_dir,".env"))


class Database:
    def row_insertion(self):
        connection = mysql.connector.connect(host=os.getenv('db_host'),
                                             user=os.getenv('db_user'),
                                             port=3306,
                                             passwd=os.getenv('db_passwd'),
                                             db=os.getenv('dbname'))
        return connection

    def table_insertion(self):
        conn = create_engine(
            "mysql+pymysql://{username}:{password}@{host}:3306/{database}".format(
                username=os.getenv("db_user"),
                password=os.getenv("db_passwd"),
                host=os.getenv("db_host"),
                database=os.getenv("dbname"),
            )
        )
        return conn