# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 12:18:21 2020

@author: Richie
"""

import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def collect_location_wise_count(url,days = 300):
    """collect_location_wise_count() function takes two arguments;
    the url(where the data is stored in json format) and period
    for the descriptive analysis. Default days is 300.
    """
    # check if the days argument is present or not; by default days is 300
    
    response = requests.get(url)  
    rows= response.json()['data']
    company = [rows[i][0] for i in range(len(rows))]
    location = [rows[i][1] for i in range(len(rows))]
    email = [rows[i][2] for i in range(len(rows))]
    date = [rows[i][3] for i in range(len(rows))]
    data = pd.DataFrame(np.column_stack([company,location,email,date]),columns = ['Company_Name','Location','Email','Application_Date'])
    # Change the format of application date and replace the none values by a year back date
    data['Application_Date'] = [pd.to_datetime(data['Application_Date'][i]) if data['Application_Date'][i] != None else pd.to_datetime(datetime.now()-timedelta(days = 365)) for i in range(len(data))]
    # extract the month and add the month column to the existing dataframe data
    month = [data['Application_Date'][i].month for i in range(len(data))]
    year = [data['Application_Date'][i].year for i in range(len(data))]
    # Add the columns to the existing dataframe
    data['month'] = month
    data['year'] = year
    # filter the dataset (default only last 300 days is taken)
    start_date = pd.to_datetime(datetime.now())
    end_date = pd.to_datetime(datetime.now()-timedelta(days = int(days)))
    index = [ i for i in range(len(data)) if (data['Application_Date'][i].value < start_date.value) & (data['Application_Date'][i].value > end_date.value)]
    filtered_data = data.loc[index]
    
    # group by operation location wise
    filtered_data.columns
    location_wise = filtered_data.groupby(['month','Location'])
    location_wise_df = pd.DataFrame(location_wise.size().reset_index(name = "Group_Count"))
    return location_wise_df

def tenure_dict(month_list):
    """tenure_dict() function takes the unique list of months in integer
       format and returns the mapping of integer and its corresponding
       month name. For example; 
                   tenure_dict1:{1: "January",
                                 10: "October",
                                 ...
                                 }
    """
    assert type(month_list) == list
    # make the dictionary for the period of analysis
    calendar_dict = {1: "January",
                    2: "February",
                    3: "March" ,
                    4: "April",
                    5: "May", 
                    6: "June", 
                    7: "July", 
                    8: "August", 
                    9: "September",
                    10: "October",
                    11: "November",
                    12: "December"
                    }
    # Instantiate the dictionary to store the months and its 
    # corresponding month label
    tenure = {}
    for i in month_list:
        tenure[i] = calendar_dict[i]
    return tenure        

if "__name__" == "__main.py__":
    collect_location_wise_count()
    tenure_dict()