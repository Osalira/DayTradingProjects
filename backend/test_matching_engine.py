#!/usr/bin/env python3
"""
Test script to verify communication with the matching engine.
This script sends stock orders to the matching engine's placeStockOrder endpoint,
which should then notify the trading service.
"""

import requests
import json
import time
import sys
import os
import logging
import argparse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def parse_args():
    parser = argparse.ArgumentParser(description='Test matching engine order placement.')
    parser.add_argument('--host', type=str, default='localhost',
                        help='Host name of the matching engine (default: localhost)')
    parser.add_argument('--port', type=int, default=4003,
                        help='Port of the matching engine (default: 4003)')
    parser.add_argument('--protocol', type=str, default='http',
                        choices=['http', 'https'], 
                        help='Protocol to use (http or https)')
    parser.add_argument('--no-verify-ssl', action='store_true',
                        help='Disable SSL certificate verification')
    parser.add_argument('--user-id', type=int, default=1,
                        help='User ID for the order')
    parser.add_argument('--stock-id', type=int, default=1,
                        help='Stock ID (Google=1, Apple=2)')
    parser.add_argument('--is-buy', action='store_true',
                        help='Make a buy order (default is sell)')
    parser.add_argument('--quantity', type=int, default=5,
                        help='Quantity of shares')
    parser.add_argument('--price', type=float, default=150.00,
                        help='Price per share for limit orders')
    parser.add_argument('--order-type', type=str, default='Limit',
                        choices=['Market', 'Limit'],
                        help='Order type (Market or Limit)')
    parser.add_argument('--token', type=str,
                        help='Authentication token (if required)')
    
    # Parse from environment if not specified on command line
    args = parser.parse_args()
    
    # Override with environment variables if present
    if "MATCHING_ENGINE_HOST" in os.environ:
        args.host = os.environ["MATCHING_ENGINE_HOST"]
    if "MATCHING_ENGINE_PORT" in os.environ:
        args.port = int(os.environ["MATCHING_ENGINE_PORT"])
    if "MATCHING_ENGINE_PROTOCOL" in os.environ:
        args.protocol = os.environ["MATCHING_ENGINE_PROTOCOL"]
    if "NO_VERIFY_SSL" in os.environ:
        args.no_verify_ssl = os.environ["NO_VERIFY_SSL"].lower() in ("true", "1", "t")
    if "AUTH_TOKEN" in os.environ:
        args.token = os.environ["AUTH_TOKEN"]
    
    return args

def test_place_order(args):
    """
    Test placing an order with the matching engine.
    """
    logger.info(f"Testing placing {'buy' if args.is_buy else 'sell'} order with matching engine")
    
    # Build the URL from components
    url = f"{args.protocol}://{args.host}:{args.port}/api/placeStockOrder"
    
    # Prepare the order payload
    payload = {
        "user_id": args.user_id,
        "stock_id": args.stock_id,
        "is_buy": args.is_buy,
        "order_type": args.order_type,
        "quantity": args.quantity,
        "price": args.price
    }
    
    # Setup headers
    headers = {
        "Content-Type": "application/json",
        "user_id": str(args.user_id)  # Add user_id as header for authentication
    }
    
    # Add authentication headers if provided
    if args.token:
        # Standard Authorization header with Bearer prefix
        headers["Authorization"] = f"Bearer {args.token}"
        logger.info(f"Added token to headers (first 20 chars): {args.token[:20]}...")
    
    # Send the order to the matching engine
    logger.info(f"Sending order to {url}")
    logger.info(f"Payload: {json.dumps(payload, indent=2)}")
    logger.info(f"Headers: {json.dumps({k: v for k, v in headers.items() if k != 'Authorization' or len(v) < 30}, indent=2)}")
    logger.info(f"SSL verification: {not args.no_verify_ssl}")
    
    try:
        response = requests.post(url, json=payload, headers=headers, verify=not args.no_verify_ssl)
        
        logger.info(f"Response status code: {response.status_code}")
        
        response_data = None
        try:
            response_data = response.json()
            logger.info(f"Response data: {json.dumps(response_data, indent=2)}")
        except:
            logger.info(f"Response text: {response.text}")
        
        # Check if the response is successful
        if response.status_code == 200:
            logger.info("Order placed successfully")
            return response_data  # Return the response data, not just True
        else:
            logger.error(f"Error placing order: {response.status_code}")
            return None
    
    except requests.exceptions.SSLError as e:
        logger.error(f"SSL Error: {str(e)}")
        logger.info("Try running with --protocol=http or --no-verify-ssl if using self-signed certificates")
        return None
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Connection Error: {str(e)}")
        logger.info("Check if the matching engine is running and the URL is correct")
        return None
    except Exception as e:
        logger.error(f"Exception while placing order: {str(e)}")
        return None

def test_cancel_order(args, order_id):
    """
    Test cancelling an order with the matching engine.
    """
    logger.info(f"Testing cancelling order {order_id} with matching engine")
    
    # Build the URL from components
    url = f"{args.protocol}://{args.host}:{args.port}/api/cancelStockTransaction"
    
    # Prepare the cancel payload
    payload = {
        "transaction_id": order_id
    }
    
    # Setup headers
    headers = {
        "Content-Type": "application/json",
        "user_id": str(args.user_id)  # Add user_id as header for authentication
    }
    
    # Add authentication headers if provided
    if args.token:
        # Standard Authorization header with Bearer prefix
        headers["Authorization"] = f"Bearer {args.token}"
    
    # Send the cancel request to the matching engine
    logger.info(f"Sending cancel request to {url}")
    logger.info(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(url, json=payload, headers=headers, verify=not args.no_verify_ssl)
        
        logger.info(f"Response status code: {response.status_code}")
        
        try:
            response_data = response.json()
            logger.info(f"Response data: {json.dumps(response_data, indent=2)}")
        except:
            logger.info(f"Response text: {response.text}")
        
        # Check if the response is successful
        if response.status_code == 200:
            logger.info("Order cancelled successfully")
            return True
        else:
            logger.error(f"Error cancelling order: {response.status_code}")
            return False
    
    except Exception as e:
        logger.error(f"Exception while cancelling order: {str(e)}")
        return False

if __name__ == "__main__":
    args = parse_args()
    
    logger.info(f"Using matching engine at {args.protocol}://{args.host}:{args.port}")
    
    # Place an order
    result = test_place_order(args)
    
    order_id = None
    if result and isinstance(result, dict):
        # The matching engine response might be structured like {'order_id': 123, 'status': 'InProgress', ...}
        # or it might be nested deeper in 'result' or other keys
        if 'order_id' in result:
            order_id = result['order_id']
        elif 'result' in result and isinstance(result['result'], dict) and 'order_id' in result['result']:
            order_id = result['result']['order_id']
    
    if order_id:
        logger.info(f"Successfully placed order with ID: {order_id}")
        # If order was placed successfully and we have an order_id, try cancelling it
        time.sleep(1)  # Wait a bit to allow the order to be processed
        test_cancel_order(args, order_id)
    else:
        logger.error("Failed to get order ID from response, can't test cancellation") 