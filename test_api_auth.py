# This Python script tests the API's token retrieval and access to a protected endpoint.

import requests
import json
import sys

# ----------------------------------------------------------------------
# STEP 1: CONFIGURE YOUR LOGIN CREDENTIALS HERE
# ----------------------------------------------------------------------
EMAIL = "akosua@gmail.com"   # <-- CHANGE THIS
PASSWORD = "worde1234"  # <-- CHANGE THIS
# ----------------------------------------------------------------------

API_TOKEN_URL = "http://127.0.0.1:8000/api/auth/token/"
API_TEAMS_URL = "http://127.0.0.1:8000/api/v1/teams/"

def get_auth_token():
    """Attempts to log in to the API to retrieve the access token."""
    print("--- 1. Attempting to retrieve token ---")
    
    login_data = {
        'email': EMAIL,
        'password': PASSWORD
    }

    try:
        response = requests.post(API_TOKEN_URL, data=login_data)
        response.raise_for_status()
        
        token_data = response.json()
        access_token = token_data.get('access')

        if access_token:
            print("SUCCESS: Token retrieved successfully.")
            return access_token
        else:
            print("ERROR: Token endpoint returned successfully, but no 'access' token found in response.")
            print("Response:", json.dumps(token_data, indent=2))
            return None

    except requests.exceptions.HTTPError as e:
        print(f"ERROR: Failed to retrieve token. HTTP Error: {e}")
        try:
            print("API Response Detail:", json.dumps(response.json(), indent=2))
        except:
            pass
        return None
    except requests.exceptions.ConnectionError:
        print(f"ERROR: Could not connect to {API_TOKEN_URL}. Is your Django server running?")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during token retrieval: {e}")
        return None

def test_teams_endpoint(token):
    """Uses the retrieved token to access a protected API endpoint."""
    print("\n--- 2. Testing Teams endpoint with token ---")
    
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    try:
        response = requests.get(API_TEAMS_URL, headers=headers)
        response.raise_for_status()

        print(f"SUCCESS: Teams endpoint accessed (HTTP {response.status_code}).")
        print(f"Teams Data Preview ({len(response.json())} items):")
        print(json.dumps(response.json()[:3], indent=2))
        return True

    except requests.exceptions.HTTPError as e:
        print(f"ERROR: Failed to access Teams endpoint. HTTP Error: {e}")
        try:
            print("API Response Detail:", json.dumps(response.json(), indent=2))
        except:
            pass
        return False
    except Exception as e:
        print(f"An unexpected error occurred during API test: {e}")
        return False


if __name__ == '__main__':
    # Check if user updated the placeholders
    if EMAIL == "your_actual_email" or PASSWORD == "your_actual_password":
        print("FATAL ERROR: Please edit the script (test_api_auth.py) and update the USERNAME and PASSWORD with valid credentials.")
        sys.exit(1)
        
    access_token = get_auth_token()
    
    if access_token:
        test_teams_endpoint(access_token)