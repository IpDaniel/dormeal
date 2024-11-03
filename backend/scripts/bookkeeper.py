import pandas as pd
from datetime import datetime
from .mvp_emailer import format_cart
import json

delivery_price = 2

def log_order_data(metadata, amount):
    """
    Logs order metadata to an Excel file with timestamp.
    
    Args:
        metadata (dict): Order metadata from Stripe payment intent
    """
    print("logging order data")
    try:
        # Convert Stripe object to dict
        metadata_dict = dict(metadata)
        
        # Create new record with timestamp
        new_record = {
            'timestamp': datetime.now(),
            'name': metadata_dict.get('name', ''),
            'phone': metadata_dict.get('phone', ''),
            'restaurant': metadata_dict.get('restaurant', ''),
            'additional_info': metadata_dict.get('additionalInfo', ''),
            'order_number': metadata_dict.get('orderNumber', 'N/A'),
            'order_type': metadata_dict.get('type', ''),
            'cart_details': format_cart(metadata_dict.get('cart', '')),
            'price': amount/100,
            'delivery_price': delivery_price,
            'stripe_fee': (((amount)*0.029) + 30)/100,
            'profit': delivery_price - ((((amount)*0.029) + 30)/100)
        }
        
        # Convert to DataFrame
        new_df = pd.DataFrame([new_record])
        
        # Try to read existing file or create new one
        try:
            df = pd.read_excel('data/order_history.xlsx')
            df = pd.concat([df, new_df], ignore_index=True)
        except FileNotFoundError:
            df = new_df
            
        # Save updated records
        df.to_excel('data/order_history.xlsx', index=False)
        
    except Exception as e:
        print(f"Error logging order metadata: {str(e)}")


# logs complete order data from the complete_order endpoint
def log_complete_order(data):
    """
    Logs order data from the complete_order endpoint to an Excel file with timestamp.
    
    Args:
        data (dict): Order data from the complete_order request
    """
    print("logging complete order data")
    try:
        # Create new record with timestamp
        amount = data.get('total')
        stripe_fee = round((((amount)*0.029) + 0.30), 2)
        profit = delivery_price - stripe_fee
        new_record = {
            'timestamp': datetime.now(),
            'name': data.get('name', ''),
            'address': data.get('address', ''),
            'phone': data.get('phone', ''),
            'restaurant': data.get('restaurant', ''),
            'cart_details': format_cart(data.get('cart', [])),
            'total': amount,
            'order_type': 'regular_order',
            'stripe_fee': stripe_fee,
            'profit': profit
        }
        
        # Convert to DataFrame
        new_df = pd.DataFrame([new_record])
        
        # Try to read existing file or create new one
        try:
            df = pd.read_excel('data/order_history.xlsx')
            df = pd.concat([df, new_df], ignore_index=True)
        except FileNotFoundError:
            df = new_df
            
        # Save updated records
        df.to_excel('data/order_history.xlsx', index=False)
        
    except Exception as e:
        print(f"Error logging complete order data: {str(e)}")


# logs delivery order data from the complete_delivery_order endpoint
def log_complete_delivery_order(data):
    """
    Logs delivery order data from the complete_delivery_order endpoint to an Excel file with timestamp.
    
    Args:
        data (dict): Order data from the complete_delivery_order request containing deliveryRequest details
    """
    print("logging complete delivery order data")
    try:
        # Extract delivery request data
        delivery_request = data.get('deliveryRequest', {})
        amount = data.get('total', 0)
        stripe_fee = round((amount * 0.029) + 0.30, 2)
        profit = delivery_price - stripe_fee
        
        # Create new record with timestamp
        new_record = {
            'timestamp': datetime.now(),
            'name': delivery_request.get('name', ''),
            'phone': delivery_request.get('phone', ''),
            'restaurant': delivery_request.get('restaurant', ''),
            'order_number': delivery_request.get('orderNumber', ''),
            'additional_info': delivery_request.get('additionalInfo', ''),
            'address': delivery_request.get('address', ''),
            'total': amount,
            'order_type': 'delivery_only',
            'stripe_fee': stripe_fee,
            'profit': profit
        }
        
        # Convert to DataFrame
        new_df = pd.DataFrame([new_record])
        
        # Try to read existing file or create new one
        try:
            df = pd.read_excel('data/order_history.xlsx')
            df = pd.concat([df, new_df], ignore_index=True)
        except FileNotFoundError:
            df = new_df
            
        # Save updated records
        df.to_excel('data/order_history.xlsx', index=False)
        
    except Exception as e:
        print(f"Error logging complete delivery order data: {str(e)}")

