import requests
import xml.etree.ElementTree as ET

# Replace these with your Qualys API credentials
username = "your_qualys_username"
password = "your_qualys_password"

# Define the API base URL
base_url = "https://qualysapi.qg3.apps.qualys.com"

# Set up API authentication
auth = requests.auth.HTTPBasicAuth(username, password)

# Set headers for XML content type
headers = {
    "Accept": "application/xml",
}

# Set the request parameters
params = {
    "action": "list",
}

# Send the request to retrieve asset groups
response = requests.get(
    f"{base_url}/api/2.0/fo/asset_group/",
    auth=auth,
    headers=headers,
    params=params,
)

# Check if the request was successful
if response.status_code == 200:
    print("Authentication test successful!")
else:
    print(f"Error: {response.status_code} - {response.text}")
