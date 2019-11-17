# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 12:14:39 2019

@author: CN261
"""

with open(r'body.html','r') as readfile:
    resume = readfile.read()
    
    
body = resume
file_to_attach = ['Resume.pdf']
from mail_mime import *

mailto("richie.chatterjee31@gmail.com",file_to_attach,body,subject_line='Aritra Chatterjee Resume DataScience Python/R Lead')

os.listdir()

# =============================================================================
# with open(r'body.html','w') as outfile:
#     outfile.write(resume)
# =============================================================================
