
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

# Validation Check
if pdfextract(os.path.join(data_dir,resume_list[1]))['corpus'] == ['']:
    pass
else:
    candidate_name = []
    page_count = []
    a = datetime.now()
    page_count = pdfextract(os.path.join(data_dir,resume_list[1]))['page_count']
    output = requirement_match(create_profile(os.path.join(data_dir,resume_list[1]),main_dir))
    b=datetime.now()
    print(b-a)
    candidate_name.append(resume_list[1].split('_')[0])
output
