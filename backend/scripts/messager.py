import smtplib
from email.message import EmailMessage
import os

CARRIERS = {
    "att": "@mms.att.net",
    "tmobile": "@tmomail.net",
    "verizon": "@vtext.com",
    "sprint": "@messaging.sprintpcs.com"
}

EMAIL = os.environ.get('EMAIL_ADDRESS')
PASSWORD = os.environ.get('EMAIL_PASSWORD')

def send_message(phone_number, carrier, subject, message_body):
    recipient = phone_number + CARRIERS[carrier]
    auth = (EMAIL, PASSWORD)

    msg = EmailMessage()
    msg['Subject'] = subject
    msg.set_content(message_body)

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(auth[0], auth[1])

    server.sendmail(auth[0], recipient, msg.as_string())

    server.quit()

send_message('13017675509', 'tmobile', ' ', 'Hello Daniel')






