
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 15:05:00 2020

@author: CN261
"""
# Resume Phrase Matcher code


#importing all required libraries

import os
from functions import pdfextract, create_profile, requirement_match
from datetime import datetime
    
#Function to read resumes from the folder one by one
main_dir = os.getcwd()
data_dir = os.path.join(main_dir,'data')
resume_list = os.listdir(data_dir)
a = datetime.now()
requirement_match(create_profile(os.path.join(data_dir,resume_list[0]),main_dir))
b=datetime.now()
print(b-a)


        

# create the profile of the given resume from the data folder
profile_output = create_profile(os.path.join(data_dir,resume_list[0]),main_dir)
#code to count words under each category and visulaize it through Matplotlib
profile_df2 = profile_df['Keyword'].groupby([profile_df['Candidate Name'], profile_df['Domain']]).count().unstack()
profile_df2.reset_index(inplace = True)

profile_df2.columns

profile_df2.fillna(0,inplace=True)
new_data = profile_df2.iloc[:,1:]
new_data.index = profile_df2['Candidate Name']
#execute the below line if you want to see the candidate profile in a csv format
sample2=new_data.to_csv('sample.csv')
