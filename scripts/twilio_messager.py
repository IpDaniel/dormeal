from twilio.rest import Client


# Your Twilio account SID and auth token
account_sid = 'AC5167e0809092e8fb37a1a8b9cf2314d7'
auth_token = 'f04b522024952b2f33be3419304e66b5'
phone_number = '+13019015786'

# Initialize Twilio client
client = Client(account_sid, auth_token)

# Send SMS
message = client.messages.create(
    body='Hello, this is a test message!',
    from_=phone_number,
    to='+15083061461'
)

print("Message SID:", message.sid)

