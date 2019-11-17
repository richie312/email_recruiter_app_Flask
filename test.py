# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 14:19:51 2019

@author: CN261
"""

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# Define these once; use them twice!
strFrom = 'richie.chatterjee31@gmail.com'
strTo = 'richie.chatterjee31@gmail.com'

# Create the root message and fill in the from, to, and subject headers
msgRoot = MIMEMultipart('related')
msgRoot['Subject'] = 'test message'
msgRoot['From'] = strFrom
msgRoot['To'] = strTo
msgRoot.preamble = 'This is a multi-part message in MIME format.'

# Encapsulate the plain and HTML versions of the message body in an
# 'alternative' part, so message agents can decide which they want to display.
msgAlternative = MIMEMultipart('alternative')
msgRoot.attach(msgAlternative)

msgText = MIMEText('This is the alternative plain text message.')
msgAlternative.attach(msgText)

# We reference the image in the IMG SRC attribute by the ID we give it below
msgText = MIMEText('{}'.format(body),'html')
msgAlternative.attach(msgText)

# This example assumes the image is in the current directory
fp = open('richie.jpg', 'rb')
msgImage = MIMEImage(fp.read())

# Define the image's ID as referenced above
# add required header data:
msgImage.add_header('Content-Disposition', 'attachment', filename='img1.png')
msgImage.add_header('X-Attachment-Id', '0')
msgImage.add_header('Content-ID', '<0>')
# read attachment file content into the MIMEBase object
# encode with base64
Encoders.encode_base64(msgImage)
# add MIMEBase object to MIMEMultipart object
msgRoot.attach(msgImage)
# Send the email (this example assumes SMTP authentication is required)
import smtplib
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", port,context=context) as server:
    server.login("richie.chatterjee31@gmail.com", "Pratyahara@123")
    server.sendmail(strFrom, strTo, msgRoot.as_string())
