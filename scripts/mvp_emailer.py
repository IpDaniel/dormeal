import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

daniel_email = 'arc.daniel42@gmail.com'
daniel_password = 'uyzo mdwk llyq azxs'
default_subject = 'New Order'

order_notify_email_list = ['arc.daniel42@gmail.com', 'ip.d@northeastern.edu', 'acrocks724@gmail.com']

#sends an email with the given message and subject to the given recipient
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

#sends an email with the given message and subject to each of the recipients in the given recipient list
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

#Formats json cart data into something easier to understand by a human:
import json

def format_order(order):
    output = []
    output.append(f"Name: {order['name']}")
    output.append(f"Address: {order['address']}")
    output.append(f"Phone: {order['phone']}")
    output.append(f"Restaurant: {order['restaurant']}")
    output.append("Cart Items:")

    for item in order['cart']:
        item_details = []
        item_details.append(f"Name: {item['name']}")
        item_details.append(f"  Quantity: {item['quantity']}")
        item_details.append(f"  Item ID: {item['id']}")
        item_details.append(f"  Base Price: ${item['basePrice']:.2f}")
        
        if item['addOns']:
            item_details.append("  Add-Ons:")
            for addon in item['addOns']:
                item_details.append(f"    - {addon['name']}: ${addon['price']:.2f}")
        else:
            item_details.append("  Add-Ons: None")
        
        if item['choices']:
            item_details.append("  Choices:")
            for choice in item['choices']:
                item_details.append(f"    - {choice['name']}: ${choice['price']:.2f}")
        else:
            item_details.append("  Choices: None")
        
        output.append("\n".join(item_details))

    output.append(f"Total: ${order['total']:.2f}")
    output.append(f"Total Minus Delivery: ${(order['total'] - 5):.2f}")
    
    return "\n".join(output)

# Example usage:
order_data = {
    'name': 'Daniel Ip',
    'address': '4326 Kentbury Dr',
    'phone': '3017675509',
    'cart': [
        {
            'id': '1',
            'name': 'Spring Rolls',
            'basePrice': 5,
            'addOns': [{'name': 'Extra Sauce', 'price': 1}],
            'choices': [],
            'quantity': 1
        },
        {
            'id': '3',
            'name': 'Grilled Chicken',
            'basePrice': 15,
            'addOns': [],
            'choices': [{'name': 'BBQ Sauce', 'price': 1}],
            'quantity': 2
        }
    ],
    'restaurant': 'Restaurant Name',
    'total': 45.66
}

formatted_order = format_order(order_data)
#print(formatted_order)
