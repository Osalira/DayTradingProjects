import requests
import json
import time

def test_token_auth():
    """
    Test token authentication with the API Gateway using both token header formats:
    1. Standard 'Authorization: Bearer <token>' format
    2. JMeter 'token: <token>' format
    """
    # Base URL for the API Gateway
    base_url = "http://localhost:4000"
    
    # Step 1: Register a new test user
    print("Step 1: Registering a new test user")
    register_payload = {
        "user_name": "testuser7",
        "password": "User@123",
        "account_type": "user",
        "name": "Test User 7",
        "email": "testuser7@example.com"
    }
    
    register_response = requests.post(
        f"{base_url}/authentication/register",
        json=register_payload
    )
    
    print(f"Register Status: {register_response.status_code}")
    try:
        register_json = register_response.json()
        print(f"Register Response: {json.dumps(register_json, indent=2)}")
    except:
        print(f"Register Raw Response: {register_response.text}")
    print("-----------------------------")
    
    # Step 2: Login to get a token
    print("Step 2: Logging in to get a token")
    login_payload = {
        "user_name": "testuser7",
        "password": "User@123"
    }
    
    login_response = requests.post(
        f"{base_url}/authentication/login",
        json=login_payload
    )
    
    print(f"Login Status: {login_response.status_code}")
    token = None
    try:
        login_json = login_response.json()
        print(f"Login Response: {json.dumps(login_json, indent=2)}")
        
        # Handle nested structure - the token could be in data.data.token or data.token
        if login_response.status_code == 200:
            if 'data' in login_json and 'data' in login_json['data'] and 'token' in login_json['data']['data']:
                token = login_json['data']['data']['token']
                print(f"Token obtained (from data.data.token): {token[:20]}...{token[-20:]}")
            elif 'data' in login_json and 'token' in login_json['data']:
                token = login_json['data']['token']
                print(f"Token obtained (from data.token): {token[:20]}...{token[-20:]}")
            else:
                print("Failed to get token from response - token not found in expected paths")
                print("Response structure:", json.dumps(login_json, indent=2))
    except Exception as e:
        print(f"Login Raw Response: {login_response.text}")
        print(f"Error parsing response: {str(e)}")
    print("-----------------------------")
    
    if not token:
        print("Token not available, can't continue tests")
        return
    
    # Small delay to ensure token is properly processed
    time.sleep(1)
    
    # Test debug endpoints before trying the protected endpoints
    print("Testing API Gateway debug endpoint")
    test_api_gateway_debug(base_url, token)
    print("-----------------------------")
    
    print("Testing Trading Service debug endpoint")
    test_trading_debug(base_url, token)
    print("-----------------------------")
    
    # Step 3: Test Authorization header format
    print("Step 3: Testing Authorization header format")
    auth_headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    print(f"Request Headers: {json.dumps(auth_headers, indent=2)}")
    
    # Enable request/response debugging 
    session = requests.Session()
    session.hooks['response'] = [lambda r, *args, **kwargs: print(f"DEBUG: Request URL: {r.request.url}")]
    
    auth_header_response = session.get(
        f"{base_url}/transaction/getWalletBalance",
        headers=auth_headers
    )
    
    print(f"Auth Header Status: {auth_header_response.status_code}")
    print(f"Response Headers: {dict(auth_header_response.headers)}")
    try:
        response_json = auth_header_response.json()
        print(f"Auth Header Response: {json.dumps(response_json, indent=2)}")
    except Exception as e:
        print(f"Auth Header Raw Response: {auth_header_response.text}")
        print(f"Error parsing response: {str(e)}")
    print("-----------------------------")
    
    # Step 4: Test token header format
    print("Step 4: Testing token header format")
    token_headers = {
        "token": token,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    print(f"Request Headers: {json.dumps(token_headers, indent=2)}")
    
    token_header_response = session.get(
        f"{base_url}/transaction/getWalletBalance",
        headers=token_headers
    )
    
    print(f"Token Header Status: {token_header_response.status_code}")
    print(f"Response Headers: {dict(token_header_response.headers)}")
    try:
        response_json = token_header_response.json()
        print(f"Token Header Response: {json.dumps(response_json, indent=2)}")
    except Exception as e:
        print(f"Token Header Raw Response: {token_header_response.text}")
        print(f"Error parsing response: {str(e)}")
    print("-----------------------------")
    
    # Step 5: Create a stock (requires admin)
    print("Step 5: Testing admin endpoint (should be forbidden)")
    admin_endpoint_response = session.post(
        f"{base_url}/setup/createStock",
        headers={"token": token},
        json={
            "symbol": "AAPL",
            "company_name": "Apple Inc.",
            "current_price": 150.0
        }
    )
    
    print(f"Admin Endpoint Status: {admin_endpoint_response.status_code}")
    try:
        response_json = admin_endpoint_response.json()
        print(f"Admin Endpoint Response: {json.dumps(response_json, indent=2)}")
    except Exception as e:
        print(f"Admin Endpoint Raw Response: {admin_endpoint_response.text}")
        print(f"Error parsing response: {str(e)}")
    print("-----------------------------")

def test_api_gateway_debug(base_url, token):
    """Test the API Gateway debug endpoint"""
    
    # Test with Authorization header
    auth_headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    auth_response = requests.get(
        f"{base_url}/debug/auth",
        headers=auth_headers
    )
    
    print(f"API Gateway Debug (Auth header) Status: {auth_response.status_code}")
    try:
        response_json = auth_response.json()
        print(f"API Gateway Debug Response: {json.dumps(response_json, indent=2)}")
    except Exception as e:
        print(f"API Gateway Debug Raw Response: {auth_response.text}")
        print(f"Error parsing response: {str(e)}")
        
    # Test with token header
    token_headers = {
        "token": token,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    token_response = requests.get(
        f"{base_url}/debug/auth",
        headers=token_headers
    )
    
    print(f"API Gateway Debug (token header) Status: {token_response.status_code}")
    try:
        response_json = token_response.json()
        print(f"API Gateway Debug Response: {json.dumps(response_json, indent=2)}")
    except Exception as e:
        print(f"API Gateway Debug Raw Response: {token_response.text}")
        print(f"Error parsing response: {str(e)}")

def test_trading_debug(base_url, token):
    """Test the Trading Service debug endpoint through the API Gateway"""
    
    # Test with Authorization header
    auth_headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    auth_response = requests.get(
        f"{base_url}/trading/debug/auth",
        headers=auth_headers
    )
    
    print(f"Trading Debug (Auth header) Status: {auth_response.status_code}")
    try:
        response_json = auth_response.json()
        print(f"Trading Debug Response: {json.dumps(response_json, indent=2)}")
    except Exception as e:
        print(f"Trading Debug Raw Response: {auth_response.text}")
        print(f"Error parsing response: {str(e)}")
        
    # Test with token header
    token_headers = {
        "token": token,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    token_response = requests.get(
        f"{base_url}/trading/debug/auth",
        headers=token_headers
    )
    
    print(f"Trading Debug (token header) Status: {token_response.status_code}")
    try:
        response_json = token_response.json()
        print(f"Trading Debug Response: {json.dumps(response_json, indent=2)}")
    except Exception as e:
        print(f"Trading Debug Raw Response: {token_response.text}")
        print(f"Error parsing response: {str(e)}")

def test_both_auth_formats():
    """
    Tests both authorization header formats sequentially to verify the fix
    """
    # Base URL for the API Gateway
    base_url = "http://localhost:4000"
    
    # Enable request/response debugging
    session = requests.Session()
    session.hooks['response'] = [lambda r, *args, **kwargs: print(f"DEBUG: Request URL: {r.request.url}\nDEBUG: Request method: {r.request.method}\nDEBUG: Request headers: {r.request.headers}")]
    
    # Step 1: Login to get a token
    print("Step 1: Logging in to get a token")
    login_payload = {
        "user_name": "testuser7",
        "password": "User@123"
    }
    
    login_response = session.post(
        f"{base_url}/authentication/login",
        json=login_payload
    )
    
    print(f"Login Status: {login_response.status_code}")
    token = None
    try:
        login_json = login_response.json()
        print(f"Login Response: {json.dumps(login_json, indent=2)}")
        
        # Handle nested structure - the token could be in data.data.token or data.token
        if login_response.status_code == 200:
            if 'data' in login_json and 'data' in login_json['data'] and 'token' in login_json['data']['data']:
                token = login_json['data']['data']['token']
                print(f"Token obtained (from data.data.token): {token[:20]}...{token[-20:]}")
            elif 'data' in login_json and 'token' in login_json['data']:
                token = login_json['data']['token']
                print(f"Token obtained (from data.token): {token[:20]}...{token[-20:]}")
            else:
                print("Failed to get token from response - token not found in expected paths")
                print("Response structure:", json.dumps(login_json, indent=2))
    except Exception as e:
        print(f"Login Raw Response: {login_response.text}")
        print(f"Error parsing response: {str(e)}")
    print("-----------------------------")
    
    if not token:
        print("Token not available, can't continue tests")
        return
    
    # Test debug endpoints
    print("Testing API Gateway debug endpoint")
    test_api_gateway_debug(base_url, token)
    print("-----------------------------")
    
    print("Testing Trading Service debug endpoint")
    test_trading_debug(base_url, token)
    print("-----------------------------")
    
    # Step 2: Test Authorization header format (Bearer token)
    print("Step 2: Testing Authorization header format (Bearer token)")
    auth_headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    print(f"Request Headers: {json.dumps(auth_headers, indent=2)}")
    
    auth_header_response = session.get(
        f"{base_url}/transaction/getWalletBalance",
        headers=auth_headers
    )
    
    print(f"Auth Header Status: {auth_header_response.status_code}")
    try:
        response_json = auth_header_response.json()
        print(f"Auth Header Response: {json.dumps(response_json, indent=2)}")
    except Exception as e:
        print(f"Auth Header Raw Response: {auth_header_response.text}")
        print(f"Error parsing response: {str(e)}")
        print(f"Response Headers: {dict(auth_header_response.headers)}")
    print("-----------------------------")
    
    # Step 3: Test token header format
    print("Step 3: Testing token header format")
    token_headers = {
        "token": token,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    print(f"Request Headers: {json.dumps(token_headers, indent=2)}")
    
    token_header_response = session.get(
        f"{base_url}/transaction/getWalletBalance",
        headers=token_headers
    )
    
    print(f"Token Header Status: {token_header_response.status_code}")
    try:
        response_json = token_header_response.json()
        print(f"Token Header Response: {json.dumps(response_json, indent=2)}")
    except Exception as e:
        print(f"Token Header Raw Response: {token_header_response.text}")
        print(f"Error parsing response: {str(e)}")
        print(f"Response Headers: {dict(token_header_response.headers)}")
    print("-----------------------------")

if __name__ == "__main__":
    test_token_auth()
    print("\n\n===== TESTING WITH NEW AUTH FORMATS =====\n\n")
    test_both_auth_formats() 