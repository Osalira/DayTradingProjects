import requests
import json

# Base URL for the API Gateway
base_url = "http://localhost:4000"

# Test registration endpoint
def test_register():
    print("Testing registration endpoint...")
    
    # Registration payload
    payload = {
        "user_name": "employee11",
        "password": "password@123",
        "account_type": "user",
        "name": "employee Corp."
    }
    
    # Send the request
    response = requests.post(
        f"{base_url}/authentication/register",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    # Print response details
    print(f"Status Code: {response.status_code}")
    print(f"Headers: {response.headers}")
    try:
        print(f"JSON Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Raw Response: {response.text}")
    print("-----------------------------")

# Test login endpoint
def test_login():
    print("Testing login endpoint...")
    
    # Login payload
    payload = {
        "user_name": "employee11",
        "password": "password@123"
    }
    
    # Send the request
    response = requests.post(
        f"{base_url}/authentication/login",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    # Print response details
    print(f"Status Code: {response.status_code}")
    print(f"Headers: {response.headers}")
    try:
        print(f"JSON Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Raw Response: {response.text}")
    print("-----------------------------")

if __name__ == "__main__":
    test_register()
    test_login() 