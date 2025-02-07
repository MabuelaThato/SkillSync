import smtplib

def send_email(sender,receiver, password, message, subject):
    server = smtplib.SMTP_SSL("smtp.gmail.com",465)
    server.ehlo()
    server.starttls
    sender = os.getenv("SENDER_EMAIL")
    
    server.login(sender, password)
    server.sendmail(sender, email , message)

    SUBJECT = subject  
    TEXT = message 
    text = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
    s.sendmail(sender, receiver, text)
    server.quit()
    