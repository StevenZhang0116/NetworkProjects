#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL

from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


host_server = 'smtp.qq.com'
sender_qq = '153503537@qq.com'
pwd = '*****mkenb****' 
sender_qq_mail = '153503537@qq.com'
receiver = ['zihanzhang0116@gmail.com','h****u@qq.com']

mail_content = ""
mail_title = 'IMAGE TEST TRAIL'


msg = MIMEMultipart('related')
msg["Subject"] = Header(mail_title, 'utf-8')
msg["From"] = sender_qq_mail
msg["To"] = Header("Receiver TEST", 'utf-8')

msgAlternative = MIMEMultipart('alternative')
msg.attach(msgAlternative)

mail_body = """
 <p>PYTHON sending test</p>
 <p>Use Python (smtplib & email packages) to send email</p>
 <p>Here is the image: </p>
 <p>![](cid:send_image)</p>
"""

msgText = (MIMEText(mail_body, 'html', 'utf-8'))
msgAlternative.attach(msgText)

fp = open('image.png', 'rb')
msgImage = MIMEImage(fp.read())
fp.close()
 
msgImage.add_header('Content-ID', '<send_image>')
msg.attach(msgImage)

smtp = SMTP_SSL(host_server)
smtp.set_debuglevel(1)
smtp.ehlo(host_server)
smtp.login(sender_qq, pwd)

smtp.sendmail(sender_qq_mail, receiver, msg.as_string())
smtp.quit()