import requests
import xml.etree.ElementTree as ET
from requests.auth import HTTPBasicAuth

# Update the base URL for the QG3 pod
QUALYS_BASE_URL = 'https://qualysapi.qg#.apps.qualys.com/api/2.0/fo/'

# Set your Qualys API username and password
QUALYS_API_USERNAME = 'your_username'
QUALYS_API_PASSWORD = 'your_password'

def create_dynamic_search_list(name):
    url = f"{QUALYS_BASE_URL}qid/search_list/dynamic/"

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Requested-With': 'Python Script',  # Add a description for the X-Requested-With header
    }

    data = {
        'action': 'create',
        'title': name,
        'global': '1',  # Set the search list as global
        'confirmed_severities': '2,3,4,5',  # Only include confirmed vulnerabilities with severity levels 2-5
        'potential_severities': '2,3,4,5'  # Also include potential vulnerabilities with severity levels 2-5
    }

    response = requests.post(
        url,
        headers=headers,
        data=data,
        auth=HTTPBasicAuth(QUALYS_API_USERNAME, QUALYS_API_PASSWORD)
    )

    if response.status_code == 200:
        xml_root = ET.fromstring(response.text)
        if xml_root.find('.//RESPONSE/CODE') is not None:
            error_code = xml_root.findtext('.//RESPONSE/CODE')
            error_msg = xml_root.findtext('.//RESPONSE/TEXT')
            print(f"Error creating search list: {error_code} - {error_msg}")
        else:
            search_list_id = xml_root.findtext('.//RESPONSE/ITEM_LIST/ITEM/VALUE')
            print(f"Created global dynamic search list '{name}' with ID {search_list_id}")
    else:
        print(f"Error creating search list: {response.status_code} - {response.text}")

if __name__ == "__main__":
    search_list_name = input("Enter the search list title: ")

    create_dynamic_search_list(search_list_name)
