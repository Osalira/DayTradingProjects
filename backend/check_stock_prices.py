#!/usr/bin/env python3
"""
Quick script to directly check stock prices from the trading service,
bypassing the API Gateway to debug potential issues.
"""

import requests
import json
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Token from testuser7
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0MDg4ODU5MiwianRpIjoiMGQzYjkwM2QtNzMzNi00NDg5LWE2Y2QtYjdkYzgxMWE5ZTUwIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJpZCI6NCwidXNlcm5hbWUiOiJ0ZXN0dXNlcjciLCJhY2NvdW50X3R5cGUiOiJ1c2VyIiwibmFtZSI6IlRlc3QgVXNlciA3IiwiZW1haWwiOiJ0ZXN0dXNlcjdAZXhhbXBsZS5jb20iLCJhY2NvdW50X2JhbGFuY2UiOjAuMH0sIm5iZiI6MTc0MDg4ODU5MiwiY3NyZiI6IjI1MWFhMTYxLTlmYjEtNDRmNC1hNTI3LTE4NmU1ODU3MDE3MiIsImV4cCI6MTc0MDg5MjE5Mn0.-VkaXTF746A6-opTU9Gwjga-_BRp7u6nmxA_gS79L-U"

def check_prices_via_gateway():
    """Check stock prices via the API Gateway"""
    url = "http://localhost:4000/transaction/getStockPrices"
    
    # Add authentication headers
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "token": TOKEN  # Add as separate token header for compatibility
    }
    
    logger.info(f"Checking stock prices via API Gateway: {url}")
    
    try:
        response = requests.get(url, headers=headers)
        logger.info(f"API Gateway response status code: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                logger.info(f"API Gateway response data: {json.dumps(data, indent=2)}")
                
                # Check if prices are present
                if 'data' in data and isinstance(data['data'], list):
                    for stock in data['data']:
                        price = stock.get('current_price')
                        stock_name = stock.get('stock_name')
                        logger.info(f"Stock {stock_name} price via Gateway: {price}")
                
                return data
            except json.JSONDecodeError:
                logger.error(f"Failed to parse API Gateway response as JSON: {response.text}")
                return None
        else:
            logger.error(f"API Gateway request failed with status {response.status_code}: {response.text}")
            return None
    except Exception as e:
        logger.error(f"Exception when contacting API Gateway: {str(e)}")
        return None

def check_prices_directly():
    """Check stock prices directly from the trading service"""
    url = "http://localhost:4002/api/transaction/getStockPrices"
    
    logger.info(f"Checking stock prices directly from Trading Service: {url}")
    
    try:
        response = requests.get(url)
        logger.info(f"Trading Service direct response status code: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                logger.info(f"Trading Service direct response data: {json.dumps(data, indent=2)}")
                
                # Check if prices are present - might have different structure from Gateway
                if isinstance(data, list):
                    # Direct response might not have success/data wrapper
                    stocks = data
                elif 'data' in data and isinstance(data['data'], list):
                    stocks = data['data']
                else:
                    stocks = []
                    
                for stock in stocks:
                    price = stock.get('current_price')
                    stock_name = stock.get('stock_name', stock.get('company_name'))
                    logger.info(f"Stock {stock_name} price directly: {price}")
                
                return data
            except json.JSONDecodeError:
                logger.error(f"Failed to parse Trading Service response as JSON: {response.text}")
                return None
        else:
            logger.error(f"Trading Service request failed with status {response.status_code}: {response.text}")
            return None
    except Exception as e:
        logger.error(f"Exception when contacting Trading Service directly: {str(e)}")
        return None

if __name__ == "__main__":
    logger.info("Checking stock prices...")
    
    # First check via API Gateway
    gateway_data = check_prices_via_gateway()
    
    # Then check directly from trading service
    direct_data = check_prices_directly()
    
    # Compare results
    if gateway_data and direct_data:
        logger.info("Comparison of stock prices between API Gateway and direct Trading Service access:")
        
        gateway_stocks = gateway_data.get('data', []) if isinstance(gateway_data, dict) else gateway_data
        direct_stocks = direct_data.get('data', []) if isinstance(direct_data, dict) else direct_data
        
        # Try to map stocks by ID for comparison
        gateway_stocks_by_id = {stock.get('stock_id'): stock for stock in gateway_stocks}
        direct_stocks_by_id = {stock.get('stock_id'): stock for stock in direct_stocks}
        
        for stock_id in set(gateway_stocks_by_id.keys()) | set(direct_stocks_by_id.keys()):
            gateway_price = gateway_stocks_by_id.get(stock_id, {}).get('current_price')
            direct_price = direct_stocks_by_id.get(stock_id, {}).get('current_price')
            
            stock_name = (gateway_stocks_by_id.get(stock_id, {}).get('stock_name') or 
                         direct_stocks_by_id.get(stock_id, {}).get('stock_name', f"Stock {stock_id}"))
            
            if gateway_price != direct_price:
                logger.info(f"⚠️ Price mismatch for {stock_name}: Gateway={gateway_price}, Direct={direct_price}")
            else:
                logger.info(f"✅ Price match for {stock_name}: {gateway_price}")
    
    logger.info("Done checking stock prices.") 