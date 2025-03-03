#!/usr/bin/env python3
"""
Test script to verify communication between matching engine and trading service.
This script simulates the matching engine's notifyTradingService function by sending 
a transaction notification directly to the trading service's processTransaction endpoint.
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
    parser = argparse.ArgumentParser(description='Test trading service notification.')
    parser.add_argument('--host', type=str, default='localhost',
                        help='Host name of the trading service')
    parser.add_argument('--port', type=int, default=4000,
                        help='Port of the service (default: 4000 for API Gateway)')
    parser.add_argument('--protocol', type=str, default='http',
                        choices=['http', 'https'], 
                        help='Protocol to use (http or https)')
    parser.add_argument('--no-verify-ssl', action='store_true',
                        help='Disable SSL certificate verification')
    parser.add_argument('--buy-user', type=int, default=1,
                        help='User ID of the buyer')
    parser.add_argument('--sell-user', type=int, default=2,
                        help='User ID of the seller')
    parser.add_argument('--stock-id', type=int, default=1,
                        help='Stock ID (Google=1, Apple=2)')
    parser.add_argument('--quantity', type=int, default=5,
                        help='Quantity of shares')
    parser.add_argument('--price', type=float, default=150.00,
                        help='Price per share')
    parser.add_argument('--system-user-id', type=int, default=0,
                        help='System user ID for authentication (used as HTTP header)')
    parser.add_argument('--token', type=str,
                        help='Authentication token (if required)')
    parser.add_argument('--notification-type', type=str, default='default',
                    help='Type of notification (e.g., new_order)')

    
    # Parse from environment if not specified on command line
    args = parser.parse_args()
    
    # Override with environment variables if present
    if "TRADING_HOST" in os.environ:
        args.host = os.environ["TRADING_HOST"]
    if "TRADING_PORT" in os.environ:
        args.port = int(os.environ["TRADING_PORT"])
    if "TRADING_PROTOCOL" in os.environ:
        args.protocol = os.environ["TRADING_PROTOCOL"]
    if "NO_VERIFY_SSL" in os.environ:
        args.no_verify_ssl = os.environ["NO_VERIFY_SSL"].lower() in ("true", "1", "t")
    if "SYSTEM_USER_ID" in os.environ:
        args.system_user_id = int(os.environ["SYSTEM_USER_ID"])
    if "AUTH_TOKEN" in os.environ:
        args.token = os.environ["AUTH_TOKEN"]
    
    return args

def test_process_transaction(args):
    """
    Test the processTransaction endpoint in the trading service.
    
    Note: This should be accessed through the API Gateway (port 4000)
    rather than directly to the trading service (port 8000).
    The API Gateway handles authentication and proxying.
    """
    logger.info("Testing processTransaction endpoint")
    
    # Build the URL from components - use API Gateway path without 'api/' prefix
    url = f"{args.protocol}://{args.host}:{args.port}/transaction/processTransaction"
    
    # Prepare the transaction notification payload
    payload = {
        "buy_user_id": args.buy_user,
        "sell_user_id": args.sell_user,
        "stock_id": args.stock_id,
        "quantity": args.quantity,
        "price": args.price,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S")
    }
    
    # Setup headers
    headers = {
        "Content-Type": "application/json",
    }
    
    # Add authentication headers if provided
    if args.system_user_id >= 0:
        # Try both header formats that the authentication code looks for
        headers["user_id"] = str(args.system_user_id)  # This matches the 'user_id' the authentication looks for
    
    if args.token:
        # Standard Authorization header with Bearer prefix
        headers["Authorization"] = f"Bearer {args.token}"
        
        # Also include token as a separate header for JMeter tests
        headers["token"] = args.token
        
        logger.info(f"Added token to headers (first 20 chars): {args.token[:20]}...")
    
    # Send the notification to the trading service
    logger.info(f"Sending notification to {url}")
    logger.info(f"Payload: {json.dumps(payload, indent=2)}")
    logger.info(f"Headers: {json.dumps({k: v for k, v in headers.items() if k != 'token' and k != 'Authorization' or len(v) < 30}, indent=2)}")
    logger.info(f"SSL verification: {not args.no_verify_ssl}")
    
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
            logger.info("Transaction notification successful")
            return True
        else:
            logger.error(f"Error sending transaction notification: {response.status_code}")
            return False
    
    except requests.exceptions.SSLError as e:
        logger.error(f"SSL Error: {str(e)}")
        logger.info("Try running with --protocol=http or without --verify-ssl if using self-signed certificates")
        return False
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Connection Error: {str(e)}")
        logger.info("Check if the trading service is running and the URL is correct")
        return False
    except Exception as e:
        logger.error(f"Exception while sending transaction notification: {str(e)}")
        return False

if __name__ == "__main__":
    args = parse_args()
    
    logger.info(f"Using trading service at {args.protocol}://{args.host}:{args.port}")
    
    # Run the test
    test_process_transaction(args) 