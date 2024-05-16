from flask import Flask, render_template, request
from scripts import mvp_emailer

active = True

app = Flask(__name__)

@app.route('/')
def home():
    print("home access")
    return render_template('index.html')

@app.route('/order')
def order_page():
    if active:
        return render_template('order.html')
    else:
        return render_template('inactive.html')

@app.route('/submit-order', methods=['POST'])
def submit_order():
    data = request.json
    print('New Order Placed:')
    print(data)
    email_list = mvp_emailer.order_notify_email_list
    mvp_emailer.send_email_to_multiple(email_list, str(data))
    return data

if __name__ == '__main__':
    app.run()