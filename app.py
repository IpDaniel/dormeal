from flask import Flask, render_template, request, jsonify
from scripts import mvp_emailer
import stripe

#constants
app = Flask(__name__)
active = True
stripe.api_key = 'sk_test_51PG7v4Rsh0QceLeTZzq4QceWCZEBypE4kjqIm8460Khv5abQnuzYmbgW6VHmo9s3TIw6kF2od3pRC085fkEdGlFJ00qMyOwe2u'

#returns home page at index route
@app.route('/')
def home():
    return render_template('index.html')

#renders the old order page. No longer useful
@app.route('/order')
def order_page():
    if active:
        return render_template('schools/schools.html')
    else:
        return render_template('inactive.html')

#Returns menu template. For example and dev purposes only. Not to be used in production
@app.route('/menu-template')
def menu_template():
    return render_template('menu-template.html')
    
#route all carts to this page once they are full
@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

#old submit-order function. Only works with the old form.
# Will send out email with details from old order page.
@app.route('/submit-order', methods=['POST'])
def submit_order():
    data = request.json
    print('New Order Placed:')
    print(data)
    email_list = mvp_emailer.order_notify_email_list
    mvp_emailer.send_email_to_multiple(email_list, str(data))
    return data

#creates stripe payment intent when user is directed to the checkout page
@app.route('/create-payment-intent', methods=['POST'])
def create_payment_intent():
    data = request.json
    cart = data.get('cart', [])
    total_amount = sum(
        (item['basePrice'] + sum(addon['price'] for addon in item['addOns']) + sum(choice['price'] for choice in item['choices'])) * item['quantity']
        for item in cart
    ) * 1.07 + 5.00
    intent = stripe.PaymentIntent.create(
        amount=int(total_amount * 100),  # amount in cents
        currency='usd',
    )
    return jsonify(clientSecret=intent.client_secret)

#processes the order on an existing payment intent
@app.route('/complete-order', methods=['POST'])
def complete_order():
    data = request.json
    name = data.get('name')
    address = data.get('address')
    phone = data.get('phone')
    cart = data.get('cart')
    restaurant = data.get('restaurant')
    total = data.get('total')
    
    # Here you can save the order to your database
    # Example: save_order(name, address, phone, cart)
    print(f"NEW ORDER: {name}, {address}, {phone}, {restaurant}, ${str(total)}, {str(cart)}")

    email_list = mvp_emailer.order_notify_email_list
    mvp_emailer.send_email_to_multiple(email_list, mvp_emailer.format_order(data))

    return jsonify({'status': 'success'})



"""
PAGE ROUTES:
ROUTES DEALING WITH FILE STRUCTURE NAVIGATION FOR FINDING SPECIFIC RESTAURANTS AT SPECIFIC SCHOOLS
FOR THE MVP ARE LISTED BELOW
"""

#       <---CHOOSE RESTAURANT PAGES--->

#Template
"""
@app.route('/school-name')
def school_name():
    if active:
        return render_template('schools/school-name/school-name.html')
    else:
        return render_template('inactive.html')
"""

#Northeastern choose-restaurant page
@app.route('/northeastern-university')
def northeastern_university():
    if active:
        return render_template('schools/northeastern-university/northeastern-university.html')
    else:
        return render_template('inactive.html')
    

#UMD choose-restaurant page
@app.route('/university-of-maryland')
def university_of_maryland():
    if active:
        return render_template('schools/university-of-maryland/university-of-maryland.html')
    else:
        return render_template('inactive.html')


#           <---RESTAURANT MENUS--->

#Template
"""
@app.route('/school-name/restaurant-name')
def school_name_restaurant_name():
    if active:
        return render_template('schools/school-name/restaurants/restaurant-name.html')
    else:
        return render_template('inactive.html')
"""

#Northeastern Five Guys
@app.route('/northeastern-university/five-guys')
def northeastern_university_five_guys():
    if active:
        return render_template('schools/northeastern-university/restaurants/five-guys.html')
    else:
        return render_template('inactive.html')
    

#Northeastern Wings Over
@app.route('/northeastern-university/wings-over-boston')
def northeastern_university_wings_over_boston():
    if active:
        return render_template('schools/northeastern-university/restaurants/wings-over-boston.html')
    else:
        return render_template('inactive.html')



#Northeastern El Jefe's
@app.route('/northeastern-university/el-jefes-taqueria')
def northeastern_university_el_jefes_taqueria():
    if active:
        return render_template('schools/northeastern-university/restaurants/el-jefes-taqueria.html')
    else:
        return render_template('inactive.html')

#runs the app
if __name__ == '__main__':
    app.run()
