# Import smtplib for the actual sending function
import smtplib

# Import sys to take in text from shell script
import sys

# Import the email modules we'll need
from email.message import EmailMessage

# Open the plain text file whose name is in textfile for reading.
textfile = 'Testing.txt'
with open(textfile) as fp:
    # Create a text/plain message
    msg = EmailMessage()
    msg.set_content(fp.read())

# me == the sender's email address
# you == the recipient's email address
msg['Subject'] = 'HPC Job %s has completed' % textfile
msg['From'] = 'lucas.makinen@gmail.com'
msg['To'] = 'lucas.makinen@gmail.com'
# Send the message via our own SMTP server.
s = smtplib.SMTP('localhost')
s.connect('smtp.yahoo.com', 25)
s.send_message(msg)
s.quit()