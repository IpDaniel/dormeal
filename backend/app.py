from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for
from scripts.mvp_emailer import format_cart, format_order, format_delivery_order, send_email_to_multiple, send_email, order_notify_email_list
from scripts.bookkeeper import log_order_data, log_complete_order, log_complete_delivery_order
import stripe
import os
import pandas as pd
# from dotenv import load_dotenv

# load_dotenv()  # Add this near the top of the file, after imports

#constants
app = Flask(__name__, static_folder='../frontend/static', template_folder='../frontend/templates')
active = True
test_mode = False

if test_mode:
    stripe.api_key = 'sk_test_51PG7v4Rsh0QceLeTZzq4QceWCZEBypE4kjqIm8460Khv5abQnuzYmbgW6VHmo9s3TIw6kF2od3pRC085fkEdGlFJ00qMyOwe2u'
else:
    stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')  # Stripe secret Key

#returns home page at index route
@app.route('/')
def index():
    # Log access to root endpoint
    try:
        ip_address = request.remote_addr
        access_time = pd.Timestamp.now()
        
        # Create DataFrame with new access record
        new_record = pd.DataFrame({
            'ip_address': [ip_address],
            'access_time': [access_time]
        })
        
        # Try to read existing file or create new one if it doesn't exist
        try:
            df = pd.read_excel('data/root_access.xlsx')
            df = pd.concat([df, new_record], ignore_index=True)
        except FileNotFoundError:
            df = new_record
            
        # Save updated records
        df.to_excel('data/root_access.xlsx', index=False)
    except Exception as e:
        print(f"Error logging access: {str(e)}")
    return render_template('index.html')

@app.route('/test-mode')
def get_test_mode():
    return jsonify({'test_mode': test_mode})

#renders the old order page. No longer useful
@app.route('/order')
def order_page():
    return redirect(url_for('northeastern_university'))

#Returns menu template. For example and dev purposes only. Not to be used in production
@app.route('/menu-template')
def menu_template():
    return render_template('frontend/templates/menu-template.html')


# sends email to update us when someone wants to get notified if we're active
@app.route('/notify-request', methods=['POST'])
def notify_request():
    data = request.json
    contact_info = data.get('info')
    send_email('arc.daniel42@gmail.com', str(contact_info), 'Dormeal - New Notify Request')
    return jsonify({'status': 'success'})


# sends email to update us when someone wants a new restaurant
@app.route('/restaurant-request', methods=['POST'])
def restaurant_request():
    data = request.json
    email = str(data.get('email'))
    restaurant = str(data.get('restaurant'))
    send_email('arc.daniel42@gmail.com', f"Email: {email}\nRestaurant: {restaurant}", 'Dormeal - New Restaurant Request')
    return jsonify({'status': 'success'})
    
# route all carts to this page once they are full
@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

#route for delivery-only checkout
@app.route('/delivery-only-checkout')
def delivery_only_checkout():
    return render_template('delivery-only-checkout.html')

# old submit-order function. Only works with the old form.
# Will send out email with details from old order page.
@app.route('/submit-order', methods=['POST'])
def submit_order():
    data = request.json
    print('New Order Placed:')
    print(data)
    print("datatype: " + type(data))
    email_list = order_notify_email_list
    send_email_to_multiple(email_list, str(data))
    return data

#creates stripe payment intent when user is directed to the checkout page
@app.route('/create-payment-intent', methods=['POST'])
def create_payment_intent():
    data = request.json
    if 'deliveryRequest' in data:
        print('creating delivery-only payment intent')
        # Handle delivery-only request
        delivery_request = data['deliveryRequest']
        amount = data['amount']  # Amount in cents
        intent = stripe.PaymentIntent.create(
            amount=200,
            currency='usd',
            metadata={
                'name': delivery_request['name'],
                'phone': delivery_request['phone'],
                'restaurant': delivery_request['restaurant'],
                'orderNumber': delivery_request['orderNumber'],
                'additionalInfo': delivery_request['additionalInfo'],
                'type': 'delivery_only'
            },
            statement_descriptor_suffix=''.join(char for char in delivery_request['restaurant'][:22] if char.isalnum()).upper()
        )
    else:
        print('creating normal cart payment intent')
        cart = data.get('cart', [])
        restaurant = data.get('restaurant', '')
        name = data.get('name', '')
        phone = data.get('phone', '')
        additional_info = data.get('additionalInfo', '')
        
        total_amount = sum(
            (item['basePrice'] + sum(addon['price'] for addon in item['addOns']) + sum(choice['price'] for choice in item['choices'])) * item['quantity']
            for item in cart
        ) * 1.07 + 2.00
        
        intent = stripe.PaymentIntent.create(
            amount=int(total_amount * 100),  # amount in cents
            currency='usd',
            metadata={
                'name': name,
                'phone': phone,
                'restaurant': restaurant,
                'additionalInfo': additional_info,
                'orderNumber': None,
                'type': 'regular_order',
                'cart': format_cart(cart)  # Converting cart to string since metadata must be string values
            },
            statement_descriptor_suffix=''.join(char for char in restaurant[:22] if char.isalnum()).upper()
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
    
    # Log the order data
    log_complete_order(data)
    
    print(f"NEW ORDER: {name}, {address}, {phone}, {restaurant}, ${str(total)}, {str(cart)}")

    email_list = order_notify_email_list
    send_email_to_multiple(email_list, format_order(data))

    return jsonify({'status': 'success'})

@app.route('/complete-delivery-order', methods=['POST'])
def complete_delivery_order():
    data = request.json
    delivery_request = data.get('deliveryRequest', {})
    total = data.get('total', 0)

    # Here you can save the order to your database or process it as needed
    print(f"NEW DELIVERY ORDER: {delivery_request['name']}, {delivery_request['phone']}, {delivery_request['restaurant']}, ${total}, Order Number: {delivery_request['orderNumber']}")

    email_list = order_notify_email_list
    send_email_to_multiple(email_list, format_delivery_order(data))

    log_complete_delivery_order(data)

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
