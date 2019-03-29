# -*- coding: utf-8 -*-
"""
Created on Thu Jan 10 17:12:40 2019

@author: Richie
"""
import pandas as pd
import csv
import time
import os
import glob
os.chdir(r"C:\Users\Richie\Desktop\Email_Python")


"""Collect data """


Last_Count = len(glob.glob1(r"C:\Users\Richie\Desktop\Email_Python",
                            "*.csv"))


dataframe = pd.read_csv("data_as_on{}.csv".format(Last_Count))


print("Please enter the Company's/Consultant Name")
Company = input()
print("Please enter the Location Name")
Location = input()
print("Please enter the sender's email address")
email = input()

df2 = pd.DataFrame({'Location': Location, 'Company':Company,
                    'Email':Email},index = range(len(dataframe)))


Frame = dataframe.append(df2)

Frame.to_csv("data_as_on{}.csv".format(len(Frame)))
