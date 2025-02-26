import smtplib,os

def send_email(sender,receiver, password, message, subject):
    server = smtplib.SMTP_SSL("smtp.gmail.com",465)
    server.ehlo()
    server.starttls
    
    server.login(sender, password)

    SUBJECT = subject  
    TEXT = message 
    text = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
    server.sendmail(sender, receiver, text)
    server.quit()
    