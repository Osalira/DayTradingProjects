#!/usr/bin/env python3
import requests
import json
import time

# Configuration
API_URL = "http://localhost:4000/engine/placeStockOrder"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0MDkwNzAwNCwianRpIjoiZTA3OWMyZGMtMGNkNC00YWY5LWFlYzctMTdlZDNiNDc4NTE3IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJpZCI6MywidXNlcm5hbWUiOiJGaW5hbmNlR3VydSIsImFjY291bnRfdHlwZSI6InVzZXIiLCJuYW1lIjoiVGhlIEZpbmFuY2UgR3VydSIsImVtYWlsIjoiRmluYW5jZUd1cnVAZXhhbXBsZS5jb20iLCJhY2NvdW50X2JhbGFuY2UiOjAuMH0sIm5iZiI6MTc0MDkwNzAwNCwiY3NyZiI6ImU2Njk1NmM3LTRjMGQtNGZjOC1hZTIzLTk0YTZhYjZiNDE2NCIsImV4cCI6MTc0MDkxMDYwNH0.I5n7R97iBJ3r_0O-Lq7hN96Etxp11noFYld5KqpeWpM"

# Order data
order_data = {
    "stock_id": 1,
    "is_buy": True,
    "order_type": "Market",
    "quantity": 5
}

# Headers
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {TOKEN}"
}

def place_order():
    try:
        # Make the POST request
        print(f"Sending order request to {API_URL}")
        print(f"Order data: {json.dumps(order_data, indent=2)}")
        
        response = requests.post(API_URL, json=order_data, headers=headers)
        
        # Print response details
        print(f"Response status code: {response.status_code}")
        
        try:
            response_json = response.json()
            print(f"Response JSON: {json.dumps(response_json, indent=2)}")
        except ValueError:
            print(f"Response text (not JSON): {response.text}")
            
        # Wait for the order to be processed
        print("\nWaiting 3 seconds for order to be processed...")
        time.sleep(3)
            
        # Now check for transactions
        if response.status_code == 200:
            print("\nChecking for transactions after order placement...")
            get_transactions()
    
    except Exception as e:
        print(f"Error placing order: {str(e)}")

def get_transactions():
    try:
        transactions_url = "http://localhost:4000/transaction/getStockTransactions"
        
        print(f"Sending request to {transactions_url}")
        
        response = requests.get(transactions_url, headers=headers)
        
        print(f"Transactions response status code: {response.status_code}")
        
        try:
            response_json = response.json()
            print(f"Transactions response: {json.dumps(response_json, indent=2)}")
            
            # Print detailed information about the first transaction
            if response.status_code == 200 and 'data' in response_json and response_json['data']:
                first_tx = response_json['data'][0]
                print("\n====== TRANSACTION DETAILS ======")
                print(f"Transaction ID: {first_tx.get('id')}")
                print(f"Order Type: {first_tx.get('order_type')}")
                print(f"Status: {first_tx.get('order_status')}")
                print(f"Stock Price: {first_tx.get('stock_price')}")
                print(f"Is Buy: {first_tx.get('is_buy')}")
                print(f"Parent Transaction ID: {first_tx.get('parent_stock_tx_id')}")
                print(f"Wallet Transaction ID: {first_tx.get('wallet_tx_id')}")
                print(f"External Order ID: {first_tx.get('external_order_id')}")
                print("=================================")
        except ValueError:
            print(f"Response text (not JSON): {response.text}")
            
    except Exception as e:
        print(f"Error getting transactions: {str(e)}")

if __name__ == "__main__":
    place_order() 