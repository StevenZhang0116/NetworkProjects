# NetworkProjects

**socket_smtp.py**: Send an email, with an attachment or image, from a python script. Be able to specify the server name/IP address and allow for any attachment and message body to be sent using MIME. Demonstrate SMTP (Simple Mail Transfer Protocol) via socket programming and MIME (Multipurpose Internet Mail Extensions) protocol, rather than referring to existed packages like **smtplib** or **email**. Instantiate the idea by QQ-mail. Others, like Gmail or 126 mail, could use default port 25. TCP/IP 3-way handshake is important. 

**attachment.py & image.py**: Use MIMEMultipart() to instantiate the email, then use MIMEText/MIMEImage to respectively attach the (multiple) files, finally send the email by smtplib.smtp. For the image, the external link does not work for most mail service providers, so we should attach it directly. 
