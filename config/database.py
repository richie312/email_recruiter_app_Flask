import os
import json
import mysql.connector
import mysql
from src.src_context import root_dir
from dotenv import load_dotenv
""" decrypt the database details"""
load_dotenv(os.path.join(root_dir,".env"))


def db_connection():
    connection = mysql.connector.connect(host=os.getenv('db_host'),
                                         user=os.getenv('db_user'),
                                         port=3306,
                                         passwd=os.getenv('db_passwd'),
                                         db=os.getenv('dbname'))
    return connection