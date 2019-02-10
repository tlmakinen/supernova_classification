import smtplib

from smtplib import SMTP as SMTP 

gmail_user = 'lucas.makinen@gmail.com'  
gmail_password = 'FinnkiDlo97!'

sent_from = gmail_user  
to = ['tlmakinen@yahoo.com']  
subject = 'HPC Job has completed'  
body = 'Hey, wazzup?'

email_text = """\  
From: %s  
To: %s  
Subject: %s

%s
""" % (sent_from, ", ".join(to), subject, body)


#conn = SMTP(host=SMTPserver, port=587)

#try:  
server = smtplib.SMTP('smtp.gmail.com', 587)
server.ehlo()
server.starttls()
server.ehlo
server.login(gmail_user, gmail_password)
server.sendmail(sent_from, to, email_text)
server.close()

print('Email sent!')
#except:  
    #print('Something went wrong...')