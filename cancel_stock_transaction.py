#!/usr/bin/env python3
import requests
import json
import sys
import logging
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
API_URL = "http://localhost:4000/engine/cancelStockTransaction"
# Direct URL to the matching engine - CORRECTED PATH
DIRECT_ENGINE_URL = "http://localhost:4003/api/cancelStockTransaction"
AUTH_URL = "http://localhost:4000/authentication/login"

# Default credentials - replace with your own if needed
DEFAULT_USERNAME = "VanguardETF"
DEFAULT_PASSWORD = "Vang@123"

def login(username=DEFAULT_USERNAME, password=DEFAULT_PASSWORD):
    """
    Logs in to get a fresh token.
    """
    login_data = {
        "username": username,
        "password": password
    }
    
    logger.info(f"Logging in as {username} to get a fresh token...")
    
    try:
        response = requests.post(AUTH_URL, json=login_data)
        if response.status_code == 200:
            token_data = response.json()
            # The token is nested in data.token
            if token_data.get("success") and "data" in token_data and "token" in token_data["data"]:
                token = token_data["data"]["token"]
                logger.info("Login successful! Token received.")
                return token
            else:
                logger.error(f"Login response did not contain the expected token structure: {json.dumps(token_data)}")
                return None
        else:
            logger.error(f"Login failed with status code {response.status_code}: {response.text}")
            return None
    except Exception as e:
        logger.error(f"Login request failed: {str(e)}")
        return None

def cancel_with_stock_tx_id(transaction_id, token):
    """
    Attempts to cancel a transaction using the stock_tx_id parameter.
    """
    # Prepare headers with authentication token
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
        "token": token  # Include both formats for compatibility
    }
    
    # Prepare the request payload
    payload = {
        "stock_tx_id": str(transaction_id)
    }
    
    # Debugging output
    logger.info(f"Sending cancel request with stock_tx_id to {API_URL}")
    logger.info(f"Headers: {json.dumps({k: v[:20]+'...' if k in ['Authorization', 'token'] else v for k, v in headers.items()})}")
    logger.info(f"Payload: {json.dumps(payload)}")
    
    # Make the request
    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        
        # Print response information
        logger.info(f"Response status code: {response.status_code}")
        
        try:
            response_data = response.json()
            logger.info(f"Response data: {json.dumps(response_data, indent=2)}")
            return response_data
        except json.JSONDecodeError:
            logger.error(f"Response was not valid JSON: {response.text}")
            return {"success": False, "error": "Invalid JSON response", "raw_response": response.text}
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {str(e)}")
        return {"success": False, "error": str(e)}

def cancel_with_transaction_id(transaction_id, token):
    """
    Attempts to cancel a transaction using the transaction_id parameter.
    """
    # Prepare headers with authentication token
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
        "token": token  # Include both formats for compatibility
    }
    
    # Prepare the request payload - using an INTEGER for transaction_id
    payload = {
        "transaction_id": int(transaction_id)  # IMPORTANT: The Go code expects an int, not a string
    }
    
    # Debugging output
    logger.info(f"Sending cancel request with transaction_id to {API_URL}")
    logger.info(f"Headers: {json.dumps({k: v[:20]+'...' if k in ['Authorization', 'token'] else v for k, v in headers.items()})}")
    logger.info(f"Payload: {json.dumps(payload)}")
    
    # Make the request
    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        
        # Print response information
        logger.info(f"Response status code: {response.status_code}")
        
        try:
            response_data = response.json()
            logger.info(f"Response data: {json.dumps(response_data, indent=2)}")
            return response_data
        except json.JSONDecodeError:
            logger.error(f"Response was not valid JSON: {response.text}")
            return {"success": False, "error": "Invalid JSON response", "raw_response": response.text}
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {str(e)}")
        return {"success": False, "error": str(e)}

def cancel_direct_with_matching_engine(transaction_id):
    """
    Attempts to cancel a transaction by directly calling the matching engine API.
    Now using a string for transaction_id to test the updated handler.
    """
    # Prepare headers
    headers = {
        "Content-Type": "application/json",
        "user_id": "1"  # Add user_id header for authentication
    }
    
    # Prepare the request payload - using a STRING for transaction_id
    # The Go code now handles string conversion
    payload = {
        "transaction_id": str(transaction_id)  # Convert to string explicitly
    }
    
    # Debugging output
    logger.info(f"Sending direct cancel request to matching engine at {DIRECT_ENGINE_URL}")
    logger.info(f"Headers: {json.dumps(headers)}")
    logger.info(f"Payload: {json.dumps(payload)}")
    
    # Make the request
    try:
        response = requests.post(DIRECT_ENGINE_URL, json=payload, headers=headers)
        
        # Print response information
        logger.info(f"Direct response status code: {response.status_code}")
        
        try:
            response_data = response.json()
            logger.info(f"Direct response data: {json.dumps(response_data, indent=2)}")
            # For direct connection to matching engine, success is determined by status code + response message
            if response.status_code == 200 and "message" in response_data:
                response_data["success"] = True
            return response_data
        except json.JSONDecodeError:
            logger.error(f"Direct response was not valid JSON: {response.text}")
            return {"success": False, "error": "Invalid JSON response", "raw_response": response.text}
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Direct request failed: {str(e)}")
        return {"success": False, "error": str(e)}


def main():
    # Get transaction ID from command line if provided
    transaction_id = 1
    if len(sys.argv) > 1:
        try:
            transaction_id = int(sys.argv[1])
        except ValueError:
            logger.error(f"Invalid transaction ID: {sys.argv[1]}. Using default ID: 1")
    
    logger.info(f"Attempting to cancel stock transaction with ID: {transaction_id}")
    
    # Get a fresh authentication token
    token = login()
    if not token:
        logger.error("Failed to get authentication token. Will try only the direct engine connection.")
        # Skip API gateway tests if token is None
        direct_only = True
    else:
        direct_only = False
    
    # First try with stock_tx_id via API gateway (if token is available)
    if not direct_only:
        logger.info("ATTEMPT #1: Using stock_tx_id parameter via API gateway")
        result1 = cancel_with_stock_tx_id(transaction_id, token)
        success1 = result1.get("success", False)
        
        if success1:
            logger.info("✅ Cancellation successful with stock_tx_id parameter via API gateway!")
            return
        
        # Wait a moment before the next attempt
        time.sleep(1)
        
        # Try with transaction_id via API gateway
        logger.info("\nATTEMPT #2: Using transaction_id parameter (as INTEGER) via API gateway")
        result2 = cancel_with_transaction_id(transaction_id, token)
        success2 = result2.get("success", False)
        
        if success2:
            logger.info("✅ Cancellation successful with transaction_id parameter via API gateway!")
            return
        
        # Wait a moment before the next attempt
        time.sleep(1)
    else:
        logger.info("Skipping API gateway tests due to missing token.")
    
    # Try direct connection to matching engine
    logger.info("\nATTEMPT #3: Direct connection to matching engine (as INTEGER)")
    result3 = cancel_direct_with_matching_engine(transaction_id)
    success3 = result3.get("success", False)
    
    if success3:
        logger.info("✅ Cancellation successful with direct matching engine connection!")
        return
    elif result3.get("message") == "Order cancelled successfully":
        logger.info("✅ Cancellation successful with direct matching engine connection!")
        return
    
    # If all attempts failed
    logger.error("❌ All cancellation attempts failed!")
    
    # Suggest next steps
    logger.info("\nSuggested troubleshooting steps:")
    logger.info("1. Check if the transaction ID exists and is valid")
    logger.info("2. Check if the order is in a cancellable state (must be InProgress or Partially_complete)")
    logger.info("3. Verify that the API Gateway is correctly forwarding requests to the matching engine")
    logger.info("4. Check the matching engine logs for more details about the error")


if __name__ == "__main__":
    main() 