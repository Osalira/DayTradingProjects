#!/usr/bin/env python3
"""
Test script to verify that stock prices are updated from transactions.
This script simulates the matching engine's notifyTradingService function by sending 
a transaction notification to the trading service's processTransaction endpoint.
"""

import requests
import json
import time
import sys
import os
import logging
import argparse
import random
import traceback

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Default token from recent test user (testuser7)
DEFAULT_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0MDg4MzQxMCwianRpIjoiYmEzNzY5NTctZjc2MS00YzJjLTk3NmItYzczOGQ5YTRjYzZjIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJpZCI6NCwidXNlcm5hbWUiOiJ0ZXN0dXNlcjciLCJhY2NvdW50X3R5cGUiOiJ1c2VyIiwibmFtZSI6IlRlc3QgVXNlciA3IiwiZW1haWwiOiJ0ZXN0dXNlcjdAZXhhbXBsZS5jb20iLCJhY2NvdW50X2JhbGFuY2UiOjAuMH0sIm5iZiI6MTc0MDg4MzQxMCwiY3NyZiI6IjA3YTBiZTFmLWNlZjgtNDE4Ni05ZTQxLTZiOTFjYTk5NzZhMyIsImV4cCI6MTc0MDg4NzAxMH0.Ai1DeIoBpUdARolRpxSVhFwY9g1psWjyYkjpUydRYgs"

def parse_args():
    parser = argparse.ArgumentParser(description='Test stock price update mechanism.')
    parser.add_argument('--host', type=str, default='localhost',
                        help='Host name of the API Gateway (default: localhost)')
    parser.add_argument('--port', type=int, default=4000,
                        help='Port of the API Gateway (default: 4000)')
    parser.add_argument('--protocol', type=str, default='http',
                        choices=['http', 'https'], 
                        help='Protocol to use (http or https)')
    parser.add_argument('--no-verify-ssl', action='store_true',
                        help='Disable SSL certificate verification')
    parser.add_argument('--buy-user', type=int, default=4,
                        help='User ID of the buyer (default: 4 for testuser7)')
    parser.add_argument('--sell-user', type=int, default=1,
                        help='User ID of the seller')
    parser.add_argument('--stock-id', type=int, default=1,
                        help='Stock ID (Google=1, Apple=2)')
    parser.add_argument('--quantity', type=int, default=5,
                        help='Quantity of shares')
    parser.add_argument('--price', type=float, default=None,
                        help='Price per share (if not specified, a random price will be generated)')
    parser.add_argument('--system-user-id', type=int, default=4,
                        help='System user ID for authentication (used as HTTP header)')
    parser.add_argument('--token', type=str, default=DEFAULT_TOKEN,
                        help='Authentication token (default: provided test token)')
    
    return parser.parse_args()

def check_current_price(args):
    """Check the current price of the stock before sending the transaction"""
    url = f"{args.protocol}://{args.host}:{args.port}/transaction/getStockPrices"
    
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {args.token}",
        "user_id": str(args.system_user_id)
    }
    
    try:
        response = requests.get(url, headers=headers, verify=not args.no_verify_ssl)
        
        if response.status_code == 200:
            try:
                response_data = response.json()
                logger.debug(f"Stock prices response: {json.dumps(response_data, indent=2)}")
                
                # Handle nested response structure
                stocks = response_data.get('data', [])
                if not stocks and isinstance(response_data, list):
                    # Handle case where response might be a direct array
                    stocks = response_data
                
                # Find our stock
                for stock in stocks:
                    if int(stock.get('stock_id')) == args.stock_id:
                        price = stock.get('current_price')
                        if price is not None:
                            logger.info(f"Found current price for stock ID {args.stock_id}: {price}")
                            return price
                
                logger.error(f"Stock ID {args.stock_id} not found in response")
                return None
                
            except Exception as e:
                logger.error(f"Failed to parse response: {str(e)}")
        
        logger.error(f"Failed to get current price: {response.status_code}")
        logger.error(f"Response: {response.text}")
        return None
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        return None

def send_transaction(args):
    """
    Send a transaction notification to the trading service to update the stock price.
    """
    logger.info("Sending transaction notification to update stock price")
    
    # Build the URL from components
    url = f"{args.protocol}://{args.host}:{args.port}/transaction/processTransaction"
    
    # If price not specified, generate a random price
    price = args.price
    if price is None:
        # Get current price
        current_price = check_current_price(args)
        if current_price is not None:
            # Generate a price that's within 5% of the current price
            min_price = float(current_price) * 0.95
            max_price = float(current_price) * 1.05
            price = round(random.uniform(min_price, max_price), 2)
        else:
            # Default price range
            price = round(random.uniform(130.0, 150.0), 2)
    
    # Prepare the transaction notification payload
    payload = {
        "buy_user_id": args.buy_user,
        "sell_user_id": args.sell_user,
        "stock_id": args.stock_id,
        "quantity": args.quantity,
        "price": price,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S")
    }
    
    # Setup headers
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {args.token}",
        "user_id": str(args.system_user_id)
    }
    
    # Send the notification to the trading service
    logger.info(f"Sending notification to {url}")
    logger.info(f"Payload: {json.dumps(payload, indent=2)}")
    logger.info(f"Using authentication token: {args.token[:20]}...")
    
    try:
        response = requests.post(url, json=payload, headers=headers, verify=not args.no_verify_ssl)
        
        logger.info(f"Response status code: {response.status_code}")
        
        try:
            response_data = response.json()
            logger.info(f"Response data: {json.dumps(response_data, indent=2)}")
            
            if response.status_code == 200 and response_data.get('success', False):
                logger.info("✅ Transaction notification successful!")
                return True, price
            else:
                error = response_data.get('error', 'Unknown error')
                logger.error(f"❌ Transaction failed: {error}")
                return False, price
                
        except json.JSONDecodeError:
            logger.info(f"Response text (not JSON): {response.text}")
            logger.error("❌ Invalid JSON response")
            return False, price
        
    except Exception as e:
        logger.error(f"❌ Exception occurred: {str(e)}")
        return False, price

def verify_price_update(args, expected_price):
    """Verify the stock price was updated to the transaction price"""
    logger.info("Verifying stock price was updated")
    
    # Build the URL from components
    url = f"{args.protocol}://{args.host}:{args.port}/transaction/getStockPrices"
    
    # Setup headers
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {args.token}",
        "user_id": str(args.system_user_id)
    }
    
    # Send the request
    try:
        response = requests.get(url, headers=headers, verify=not args.no_verify_ssl)
        
        logger.info(f"Response status code: {response.status_code}")
        
        try:
            response_data = response.json()
            logger.info(f"Response data: {json.dumps(response_data, indent=2)}")
            
            # Handle nested response structure
            stocks = response_data.get('data', [])
            if not stocks and isinstance(response_data, list):
                # Handle case where response might be a direct array
                stocks = response_data
            
            # Find our stock
            found_stock = False
            for stock in stocks:
                if int(stock.get('stock_id')) == args.stock_id:
                    found_stock = True
                    current_price = stock.get('current_price')
                    
                    if current_price is None:
                        logger.error(f"❌ Stock price is null for stock ID {args.stock_id}")
                        return False
                    
                    # Convert both to float for comparison if they're strings
                    if isinstance(current_price, str):
                        current_price = float(current_price)
                    
                    if isinstance(expected_price, str):
                        expected_price = float(expected_price)
                    
                    # Check if price was updated (allow small floating-point differences)
                    if abs(float(current_price) - float(expected_price)) < 0.001:
                        logger.info(f"✅ Stock price was updated correctly to {current_price}")
                        return True
                    else:
                        logger.error(f"❌ Stock price was not updated. Expected: {expected_price}, Actual: {current_price}")
                        return False
            
            if not found_stock:
                logger.error(f"❌ Stock with ID {args.stock_id} not found in response")
            return False
                
        except Exception as e:
            logger.error(f"❌ Exception in verification: {str(e)}")
            logger.error(traceback.format_exc())
            return False
        
    except Exception as e:
        logger.error(f"❌ Exception occurred: {str(e)}")
        return False

if __name__ == "__main__":
    args = parse_args()
    
    logger.info(f"Using API Gateway at {args.protocol}://{args.host}:{args.port}")
    logger.info(f"Using authentication token: {args.token[:20]}...")
    
    # Check current price before the transaction
    current_price = check_current_price(args)
    if current_price is not None:
        logger.info(f"Current stock price before transaction: {current_price}")
    
    # Send the transaction
    success, used_price = send_transaction(args)
    
    if success:
        # Wait a moment for the transaction to be processed
        time.sleep(1)
        
        # Verify the price was updated
        verify_price_update(args, used_price)
    else:
        logger.error("Failed to send transaction, can't verify price update")
        sys.exit(1) 