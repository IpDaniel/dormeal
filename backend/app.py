from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for
from scripts import mvp_emailer
import stripe
import os
from dotenv import load_dotenv

load_dotenv()  # Add this near the top of the file, after imports

#constants
app = Flask(__name__, static_folder='../frontend/static', template_folder='../frontend/templates')
active = True
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')  # Stripe secret Key

#returns home page at index route
@app.route('/')
def index():
    return render_template('index.html')

#renders the old order page. No longer useful
@app.route('/order')
def order_page():
    return redirect(url_for('northeastern_university'))

#Returns menu template. For example and dev purposes only. Not to be used in production
@app.route('/menu-template')
def menu_template():
    return render_template('frontend/templates/menu-template.html')

#sends email to update us when someone wants to get notified if we're active
@app.route('/notify-request', methods=['POST'])
def notify_request():
    data = request.json
    contact_info = data.get('info')
    mvp_emailer.send_email('arc.daniel42@gmail.com', str(contact_info), 'Dormeal - New Notify Request')
    return jsonify({'status': 'success'})

#sends email to update us when someone wants a new restaurant
@app.route('/restaurant-request', methods=['POST'])
def restaurant_request():
    data = request.json
    email = str(data.get('email'))
    restaurant = str(data.get('restaurant'))
    mvp_emailer.send_email('arc.daniel42@gmail.com', f"Email: {email}\nRestaurant: {restaurant}", 'Dormeal - New Restaurant Request')
    return jsonify({'status': 'success'})
    
#route all carts to this page once they are full
@app.route('/checkout')
def checkout():
    return render_template('frontend/templates/checkout.html')

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
    print('creating payment intent')
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
        return render_template('frontend/templates/schools/school-name/school-name.html')
    else:
        return render_template('frontend/templates/inactive.html')
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
        return render_template('frontend/templates/schools/school-name/restaurants/restaurant-name.html')
    else:
        return render_template('frontend/templates/inactive.html')
"""

#Northeastern Miscellaneous
@app.route('/northeastern-university/restaurants/alternate-restaurants')
def northeastern_miscellaneous():
    if active:
        return render_template('frontend/templates/schools/northeastern-university/restaurants/alternate-restaurants.html')
    else:
        return render_template('frontend/templates/inactive.html')


#Northeastern Five Guys
@app.route('/northeastern-university/five-guys')
def northeastern_university_five_guys():
    if active:
        return render_template('schools/northeastern-university/restaurants/five-guys.html')
    else:
        return render_template('inactive.html')

@app.route('/northeastern-university/wings-over-boston')
def northeastern_university_wings_over_boston():
    if active:
        return render_template('schools/northeastern-university/restaurants/wings-over-boston.html')
    else:
        return render_template('inactive.html')

@app.route('/northeastern-university/el-jefes-taqueria')
def northeastern_university_el_jefes_taqueria():
    if active:
        return render_template('schools/northeastern-university/restaurants/el-jefes-taqueria.html')
    else:
        return render_template('inactive.html')

@app.route('/northeastern-university/mamacita')
def northeastern_university_mamacita():
    if active:
        return render_template('schools/northeastern-university/restaurants/mamacita.html')
    else:
        return render_template('inactive.html')

@app.route('/northeastern-university/amelias-taqueria')
def northeastern_university_amelias_taqueria():
    if active:
        return render_template('schools/northeastern-university/restaurants/amelias-taqueria.html')
    else:
        return render_template('inactive.html')

@app.route('/northeastern-university/sprout')
def northeastern_university_sprout():
    if active:
        return render_template('schools/northeastern-university/restaurants/sprout.html')
    else:
        return render_template('inactive.html')

@app.route('/northeastern-university/gyro-scope')
def northeastern_university_gyro_scope():
    if active:
        return render_template('schools/northeastern-university/restaurants/gyro-scope.html')
    else:
        return render_template('inactive.html')

#runs the app
if __name__ == '__main__':
    app.run(debug=True)
