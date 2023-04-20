import requests
from requests.auth import HTTPBasicAuth
import xml.etree.ElementTree as ET

# Replace these with your Qualys API credentials
QUALYS_API_USERNAME = 'your_username'
QUALYS_API_PASSWORD = 'your_password'
# Update the base URL for the QG3 pod
QUALYS_BASE_URL = 'https://qualysguard.qg3.apps.qualys.com/api/2.0/fo/'

def create_qid_search_list(name, qid_list):
    url = f"{QUALYS_BASE_URL}qid/search_list/static/"

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Requested-With': 'Python Script',  # Add a description for the X-Requested-With header
    }

    qids = ','.join(str(qid) for qid in qid_list)
    data = {
        'action': 'create',
        'title': name,
        'qids': qids,
        'global': '1',  # Set the search list as global
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
            print(f"Created global QID-based search list '{name}' with ID {search_list_id} and QIDs: {qids}")
    else:
        print(f"Error creating search list: {response.status_code} - {response.text}")

if __name__ == "__main__":
    search_list_name = input("Enter the search list title: ")
    
    qid_input = input("Enter the QIDs to add, separated by commas: ")
    qid_list = [int(qid.strip()) for qid in qid_input.split(',')]

    create_qid_search_list(search_list_name, qid_list)
