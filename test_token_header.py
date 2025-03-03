import requests
import json
import base64
import jwt
from datetime import datetime, timedelta

def test_token_header():
    # Base URL
    base_url = "http://localhost:4000"
    # Correct JWT Secret Key
    JWT_SECRET_KEY = "daytrading_jwt_secret_key_2024"
    
    # Step 1: Register a new user
    print("Step 1: Registering a new user")
    register_payload = {
        "user_name": "testuser5",  # Use a new username
        "password": "User@123",
        "account_type": "user",  # Valid account type
        "name": "Test User",
        "email": "testuser5@example.com"  # Adding email to match schema
    }
    
    register_response = requests.post(
        f"{base_url}/authentication/register",
        json=register_payload
    )
    
    print(f"Register Status: {register_response.status_code}")
    print(f"Register Response: {json.dumps(register_response.json(), indent=2)}")
    print("-----------------------------")
    
    # Step 2: Login to get a token
    print("Step 2: Logging in to get a token")
    login_payload = {
        "user_name": "testuser5",  # Use the new username
        "password": "User@123"
    }
    
    login_response = requests.post(
        f"{base_url}/authentication/login",
        json=login_payload
    )
    
    print(f"Login Status: {login_response.status_code}")
    login_json = login_response.json()
    print(f"Login Response: {json.dumps(login_json, indent=2)}")
    print("-----------------------------")
    
    if login_response.status_code == 200 and 'token' in login_json.get('data', {}):
        token = login_json['data']['token']
        
        # Decode and print JWT token contents
        try:
            # JWT tokens have 3 parts: header.payload.signature
            token_parts = token.split('.')
            if len(token_parts) == 3:
                # Add padding for base64 decoding if needed
                def fix_padding(s):
                    padding = 4 - (len(s) % 4)
                    if padding < 4:
                        return s + ("=" * padding)
                    return s
                
                # Decode header and payload
                header_json = base64.b64decode(fix_padding(token_parts[0].replace('-', '+').replace('_', '/'))).decode('utf-8')
                payload_json = base64.b64decode(fix_padding(token_parts[1].replace('-', '+').replace('_', '/'))).decode('utf-8')
                
                print("Token Header:")
                print(json.dumps(json.loads(header_json), indent=2))
                print("Token Payload:")
                print(json.dumps(json.loads(payload_json), indent=2))
        except Exception as e:
            print(f"Error decoding token: {e}")
        print("-----------------------------")
        
        # Step 3: Create a custom token with flask-jwt-extended format
        print("Step 3: Creating a custom token with Flask-JWT-Extended format")
        
        now = datetime.utcnow()
        exp = now + timedelta(hours=1)
        
        # Create payload in Flask-JWT-Extended format
        payload = {
            "fresh": False,
            "iat": int(now.timestamp()),
            "jti": "custom-token-123456",
            "type": "access",
            "sub": str(json.dumps({
                "id": 999,
                "username": "testuser4",
                "account_type": "user",
                "name": "Test User",
                "email": "testuser4@example.com",
                "account_balance": 0.0
            })),  # Subject must be a string in PyJWT
            "nbf": int(now.timestamp()),
            "exp": int(exp.timestamp())
        }
        
        custom_token = jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")
        print(f"Custom token created: {custom_token}")
        print("-----------------------------")
        
        # Step 4: Test Authorization header with custom token
        print("Step 4: Testing Authorization header with custom token")
        auth_header_response = requests.get(
            f"{base_url}/transaction/getWalletBalance",
            headers={"Authorization": f"Bearer {custom_token}"}
        )
        
        print(f"Auth Header Status: {auth_header_response.status_code}")
        try:
            response_json = auth_header_response.json()
            print(f"Auth Header Response: {json.dumps(response_json, indent=2)}")
        except:
            print(f"Auth Header Raw Response: {auth_header_response.text}")
        print("-----------------------------")
        
        # Step 5: Test token header with custom token
        print("Step 5: Testing token header with custom token")
        token_header_response = requests.get(
            f"{base_url}/transaction/getWalletBalance",
            headers={"token": custom_token}
        )
        
        print(f"Token Header Status: {token_header_response.status_code}")
        try:
            response_json = token_header_response.json()
            print(f"Token Header Response: {json.dumps(response_json, indent=2)}")
        except:
            print(f"Token Header Raw Response: {token_header_response.text}")
        print("-----------------------------")
        
        # Step 6: Test with original token for comparison
        print("Step 6: Testing token in Authorization header (original token)")
        auth_header_response = requests.get(
            f"{base_url}/transaction/getWalletBalance",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        print(f"Auth Header Status: {auth_header_response.status_code}")
        try:
            response_json = auth_header_response.json()
            print(f"Auth Header Response: {json.dumps(response_json, indent=2)}")
        except:
            print(f"Auth Header Raw Response: {auth_header_response.text}")
        print("-----------------------------")
        
        # Step 7: Health check (no token needed)
        print("Step 7: Direct API Gateway health check (no token needed)")
        headers = {"Content-Type": "application/json"}
        health_response = requests.get(f"{base_url}/health", headers=headers)
        print(f"Health Check Status: {health_response.status_code}")
        try:
            response_json = health_response.json()
            print(f"Health Response: {json.dumps(response_json, indent=2)}")
        except:
            print(f"Health Raw Response: {health_response.text}")
        print("-----------------------------")
    else:
        print("Could not get token from login response")

if __name__ == "__main__":
    test_token_header() 