import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

daniel_email = 'arc.daniel42@gmail.com'
daniel_password = 'uyzo mdwk llyq azxs'
default_subject = 'New Order'

order_notify_email_list = ['arc.daniel42@gmail.com', 'ip.d@northeastern.edu', 'acrocks724@gmail.com']


def send_email(receiver_email, message, subject=default_subject, sender_email=daniel_email, sender_password=daniel_password):
    # Set up the SMTP server
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_name = sender_email

    # Create a multipart message
    msg = MIMEMultipart()
    msg['From'] = sender_name
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Add message body to the email
    body = message
    msg.attach(MIMEText(body, 'plain'))

    # Start TLS for security
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()

    # Login with sender email and password
    server.login(sender_email, sender_password)

    # Send email
    text = msg.as_string()
    server.sendmail(sender_email, receiver_email, text)

    # Close the SMTP server
    server.quit()




"""DO NOT USE. VERY FAULTY"""
def send_email_to_multiple(receiver_emails, message, subject=default_subject, sender_email=daniel_email, sender_password=daniel_password):
    # Set up the SMTP server
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_name = sender_email

    #Start TLS for security
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()

    # Login with sender email and password
    server.login(sender_email, sender_password)

    #for each receiver address
    for email in receiver_emails:
        # Create a multipart message
        msg = MIMEMultipart()
        msg['From'] = sender_name
        msg['To'] = email
        msg['Subject'] = subject

        # Add message body to the email
        body = message
        msg.attach(MIMEText(body, 'plain'))

        # Send email
        text = msg.as_string()
        server.sendmail(sender_email, email, text)

    # Close the SMTP server
    server.quit()