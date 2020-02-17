# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 15:40:30 2020

@author: CN261
"""

from bs4 import BeautifulSoup
import requests

url = "https://medium.com/@BhashkarKunal/conversational-ai-chatbot-using-deep-learning-how-bi-directional-lstm-machine-reading-38dc5cf5a5a3"

response = requests.get(url)
data = response.text


with open('data.html','w',encoding="utf-8") as outfile:
    outfile.write(data)

soup = BeautifulSoup(response.text,'html.parser')

