#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import smtplib
from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

host_server = 'smtp.qq.com'
sender_qq = '153503537@qq.com'
pwd = '*****mkenb****' 
sender_qq_mail = '153503537@qq.com'
receiver = 'zihanzhang0116@gmail.com'

mail_content = "This is the test trail of attachments"
mail_title = 'ATTACHMENT TEST TRAIL'

msg = MIMEMultipart()
msg["Subject"] = Header(mail_title, 'utf-8')
msg["From"] = sender_qq_mail
msg["To"] = Header("Receiver TEST", 'utf-8')

msg.attach(MIMEText(mail_content, 'html', 'utf-8'))

 
# Attached files should be stored under the same folder with the script
att1 = MIMEText(open('attach.txt', 'rb').read(), 'base64', 'utf-8')
att1["Content-Type"] = 'application/octet-stream'
att1["Content-Disposition"] = 'attachment; filename="attach.txt"'
msg.attach(att1)
 
att2 = MIMEText(open('test.txt', 'rb').read(), 'base64', 'utf-8')
att2["Content-Type"] = 'application/octet-stream'
att2["Content-Disposition"] = 'attachment; filename="test.txt"'
msg.attach(att2)


smtp = SMTP_SSL(host_server)
smtp.set_debuglevel(1)
smtp.ehlo(host_server)
smtp.login(sender_qq, pwd)

smtp.sendmail(sender_qq_mail, receiver, msg.as_string())
smtp.quit()