#!/usr/bin/env python3
import requests
import json
import logging
import argparse
import sys
import time

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger(__name__)

def login(base_url, username="VanguardETF", password="Vang@123"):
    """Login to the API and get auth token"""
    url = f"{base_url}/authentication/login"
    
    login_payload = {
        "username": username,
        "password": password,
    }
    
    logger.info(f"Logging in as {username}")
    response = requests.post(url, json=login_payload)
    
    if response.status_code != 200:
        logger.error(f"Login failed: {response.status_code} - {response.text}")
        sys.exit(1)
    
    data = response.json()
    
    # Handle nested response structure
    # The token is at data.data.token and user ID is at data.data.account.id
    if 'data' in data and isinstance(data['data'], dict):
        inner_data = data['data']
        token = inner_data.get('token')
        account = inner_data.get('account', {})
        user_id = account.get('id')
    else:
        # Fall back to original structure
        token = data.get('token')
        user_id = data.get('user_id')
    
    if not token:
        logger.error(f"Login response missing token: {data}")
        sys.exit(1)
    
    logger.info(f"Login successful. User ID: {user_id}")
    return token, user_id

def get_stock_prices(base_url, token):
    """Get current stock prices"""
    url = f"{base_url}/transaction/getStockPrices"
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    logger.info("Getting current stock prices")
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        logger.error(f"Failed to get stock prices: {response.status_code} - {response.text}")
        return None
    
    data = response.json()
    # Handle different response formats
    if isinstance(data, dict) and 'data' in data:
        return data.get('data', [])
    return data

def place_sell_order(base_url, token, user_id, stock_id=1, quantity=100, price=150.0):
    """Place a sell order for a stock"""
    # Use the matching engine endpoint directly
    # In test_matching_engine.py the endpoint is /api/placeStockOrder
    url = f"{base_url}/engine/api/placeStockOrder"
    
    order_payload = {
        "user_id": user_id,
        "stock_id": stock_id,
        "is_buy": False,  # This is a sell order
        "order_type": "Limit",
        "quantity": quantity,
        "price": price
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
        "user_id": str(user_id)
    }
    
    logger.info(f"Placing sell order for stock {stock_id} at price {price}")
    logger.info(f"Using endpoint: {url}")
    logger.info(f"Order payload: {json.dumps(order_payload)}")
    
    response = requests.post(url, json=order_payload, headers=headers)
    
    logger.info(f"Response status: {response.status_code}")
    
    if response.status_code != 200:
        logger.error(f"Failed to place sell order: {response.status_code} - {response.text}")
        return None
    
    data = response.json()
    logger.info(f"Order placed successfully: {data}")
    return data

def verify_price_update(base_url, token, stock_id, expected_price):
    """Verify the stock price was updated to the expected price"""
    # Wait longer for the price update to propagate
    logger.info(f"Waiting 3 seconds for price update to propagate...")
    time.sleep(3)
    
    # Get updated stock prices
    stocks = get_stock_prices(base_url, token)
    
    if not stocks:
        logger.error("Failed to retrieve stock prices for verification")
        return False
    
    # Find the stock by ID
    stock = next((s for s in stocks if s.get('stock_id') == stock_id), None)
    
    if not stock:
        logger.error(f"Stock with ID {stock_id} not found in response")
        return False
    
    # Convert current price to float for comparison
    current_price_str = stock.get('current_price')
    current_price = float(current_price_str) if current_price_str else None
    
    logger.info(f"Current price for stock {stock_id}: {current_price}, Expected: {expected_price}")
    
    if current_price == expected_price:
        logger.info(f"✅ Stock price was updated correctly to {current_price}")
        return True
    else:
        logger.error(f"❌ Stock price was not updated. Expected: {expected_price}, Actual: {current_price}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Test sell order price update mechanism')
    parser.add_argument('--base-url', default='http://localhost:4000', help='Base URL for the API')
    parser.add_argument('--stock-id', type=int, default=1, help='Stock ID to test (default: 1 for Google)')
    parser.add_argument('--price', type=float, default=125.0, help='Price for the sell order (should be lower than current price)')
    
    args = parser.parse_args()
    
    # Login to get token
    token, user_id = login(args.base_url)
    
    # Get initial stock prices
    initial_stocks = get_stock_prices(args.base_url, token)
    initial_stock = next((s for s in initial_stocks if s.get('stock_id') == args.stock_id), None)
    
    if initial_stock:
        logger.info(f"Initial price of stock {args.stock_id} ({initial_stock.get('stock_name')}): {initial_stock.get('current_price')}")
        
        # Convert current_price to float before comparison
        current_price = float(initial_stock.get('current_price')) if initial_stock.get('current_price') else 0
        
        # If our test price is higher than current price, warn the user
        if args.price >= current_price:
            logger.warning(f"Test price ({args.price}) is not lower than current price ({current_price})")
            logger.warning("The test may fail because the sell order won't be the best (lowest) price")
    
    # Place a sell order
    sell_order = place_sell_order(args.base_url, token, user_id, args.stock_id, 100, args.price)
    
    # Verify the price was updated
    if sell_order:
        success = verify_price_update(args.base_url, token, args.stock_id, args.price)
        if success:
            logger.info("✅ Test passed! Stock price was updated based on the sell order")
        else:
            logger.error("❌ Test failed! Stock price was not updated properly")
            sys.exit(1)

if __name__ == "__main__":
    main() 