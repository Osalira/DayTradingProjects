import requests
import json
import time

def place_sell_order():
    """
    Place a sell order without cancelling it.
    """
    # Matching engine endpoint
    url = "http://localhost:4003/api/placeStockOrder"
    
    # Order data
    order_data = {
        "user_id": 1,
        "stock_id": 1,
        "is_buy": False,  # This is a sell order
        "order_type": "Limit",
        "quantity": 10,
        "price": 140.0
    }
    
    # Headers
    headers = {
        "Content-Type": "application/json",
        "user_id": "1"
    }
    
    # Send the order request
    print(f"Sending sell order request to {url}")
    print(f"Order data: {json.dumps(order_data, indent=2)}")
    
    response = requests.post(url, json=order_data, headers=headers)
    
    print(f"Response status code: {response.status_code}")
    print(f"Response JSON: {json.dumps(response.json(), indent=2)}")
    
    # Wait for the order to be processed
    print("Waiting for order to be processed...")
    time.sleep(2)
    
    # Valid token for authentication
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0MDkwNzAwNCwianRpIjoiZTA3OWMyZGMtMGNkNC00YWY5LWFlYzctMTdlZDNiNDc4NTE3IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJpZCI6MywidXNlcm5hbWUiOiJGaW5hbmNlR3VydSIsImFjY291bnRfdHlwZSI6InVzZXIiLCJuYW1lIjoiVGhlIEZpbmFuY2UgR3VydSIsImVtYWlsIjoiRmluYW5jZUd1cnVAZXhhbXBsZS5jb20iLCJhY2NvdW50X2JhbGFuY2UiOjAuMH0sIm5iZiI6MTc0MDkwNzAwNCwiY3NyZiI6ImU2Njk1NmM3LTRjMGQtNGZjOC1hZTIzLTk0YTZhYjZiNDE2NCIsImV4cCI6MTc0MDkxMDYwNH0.I5n7R97iBJ3r_0O-Lq7hN96Etxp11noFYld5KqpeWpM"
    
    # Check for transactions after order placement
    print("Checking for transactions after order placement...")
    transaction_url = "http://localhost:4000/transaction/getStockTransactions"
    
    # Headers for transaction request including token
    auth_headers = {
        "Authorization": f"Bearer {token}",
        "token": token  # Include token in both formats for compatibility
    }
    
    transaction_response = requests.get(transaction_url, headers=auth_headers)
    print(f"Transactions response status code: {transaction_response.status_code}")
    print(f"Transactions response: {json.dumps(transaction_response.json(), indent=2)}")

if __name__ == "__main__":
    place_sell_order() 