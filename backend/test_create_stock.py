#!/usr/bin/env python3
"""
Test script to verify that user_id is correctly passed from API Gateway to Trading Service
when creating a stock. This helps test the fix for the issue where user_id was defaulting to 999.
"""

import requests
import json
import sys
import os
import logging
import argparse
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def parse_args():
    parser = argparse.ArgumentParser(description='Test createStock API with user_id propagation.')
    parser.add_argument('--host', type=str, default='localhost',
                        help='Host name of the API Gateway (default: localhost)')
    parser.add_argument('--port', type=int, default=4000,
                        help='Port of the API Gateway (default: 4000)')
    parser.add_argument('--protocol', type=str, default='http',
                        choices=['http', 'https'], 
                        help='Protocol to use (http or https)')
    parser.add_argument('--user-id', type=int, default=1,
                        help='User ID to use for the test (default: 1)')
    parser.add_argument('--stock-name', type=str, default=f"TestStock-{int(time.time())}",
                        help='Stock name to create (default: auto-generated)')
    parser.add_argument('--token', type=str,
                        help='Authentication token (if required)')
    
    return parser.parse_args()

def test_create_stock(args):
    """
    Test creating a stock through the API Gateway to verify user_id propagation.
    """
    logger.info(f"Testing create stock API with user_id: {args.user_id}")
    
    # Build the URL from components
    url = f"{args.protocol}://{args.host}:{args.port}/setup/createStock"
    
    # Prepare the request payload
    payload = {
        "stock_name": args.stock_name,
        # Note: Not including user_id in payload to test header propagation
    }
    
    # Setup headers
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "user_id": str(args.user_id)  # Add user_id header for authentication
    }
    
    # Add authentication token if provided
    if args.token:
        headers["Authorization"] = f"Bearer {args.token}"
        headers["token"] = args.token  # Also include as separate token header
    
    # Send the request to the API Gateway
    logger.info(f"Sending request to {url}")
    logger.info(f"Headers: {json.dumps({k: v for k, v in headers.items() if k not in ['Authorization', 'token'] or len(v) < 30})}")
    logger.info(f"Payload: {json.dumps(payload)}")
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        
        logger.info(f"Response status code: {response.status_code}")
        
        try:
            response_data = response.json()
            logger.info(f"Response data: {json.dumps(response_data, indent=2)}")
            
            # Check if there's information about the user ID in the response
            if 'data' in response_data and isinstance(response_data['data'], dict):
                stock_data = response_data['data']
                created_by = stock_data.get('created_by', None)
                if created_by is not None:
                    logger.info(f"Stock was created with user_id: {created_by}")
                    
                    # Verify it matches our expected user_id
                    if str(created_by) == str(args.user_id):
                        logger.info("✅ SUCCESS: Stock was created with the correct user_id!")
                    else:
                        logger.error(f"❌ FAILURE: Stock was created with incorrect user_id: {created_by}, expected: {args.user_id}")
            
            return response_data
            
        except json.JSONDecodeError:
            logger.info(f"Response text (not JSON): {response.text}")
        
        # Check if the response is successful
        if response.status_code < 400:
            logger.info("Request was successful")
            return True
        else:
            logger.error(f"Error: {response.status_code}")
            return False
    
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        return False

if __name__ == "__main__":
    args = parse_args()
    
    logger.info(f"Using API Gateway at {args.protocol}://{args.host}:{args.port}")
    
    # Run the test
    result = test_create_stock(args)
    
    if result:
        logger.info("Test completed.")
    else:
        logger.error("Test failed.")
        sys.exit(1) 