import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

# Email credentials
email_address = os.environ.get('EMAIL_ADDRESS')
email_password = os.environ.get('EMAIL_PASSWORD')

def send_email(recipient, message):
    """Send a message via email."""
    # Create a multipart message
    msg = MIMEMultipart()
    msg['From'] = email_address
    msg['To'] = recipient
    msg['Subject'] = "New Message"

    # Attach message body
    msg.attach(MIMEText(message, 'plain'))

    # Connect to SMTP server
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        # Login to email account
        smtp.login(email_address, email_password)
        # Send email
        smtp.send_message(msg)

    print("Message sent successfully!")

# Example usage
recipient = "recipient@example.com"
message = "This is a test message."
send_email(recipient, message)
