import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from dotenv import load_dotenv

load_dotenv()
email = os.getenv("EMAIL_ADDRESS")
password = os.getenv("EMAIL_PASSWORD")

def sendMail(emAddr, name, file):
    
    fromaddr = email
    toaddr = emAddr

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Student Identity QRCode"
    body = "Hello " + name +"\nAttached herein is a copy of your Identification QRcode. \nPlease keep it safe"
    msg.attach(MIMEText(body, 'plain'))

    filename = file
    attachment = open(file, "rb")

    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)
    s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    s.login(fromaddr, password)
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()




    

