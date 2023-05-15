import requests
import xml.etree.ElementTree as ET
from requests.auth import HTTPBasicAuth
from getpass import getpass

QUALYS_BASE_URL = 'https://qualysapi.qg#.apps.qualys.com/api/2.0/fo/'

def create_report_template(search_list_id, qualys_api_username, qualys_api_password):
    url = QUALYS_BASE_URL + "report/template/scan/?action=create&report_format=xml"

    headers = {
        'Content-Type': 'text/xml',
        'X-Requested-With': 'Python requests'
    }

    with open("qualys-xml-payload.xml") as file:
        xml_payload_template = file.read()

    xml_payload = xml_payload_template.format(search_list_id=search_list_id)

    response = requests.post(url, headers=headers, data=xml_payload, auth=HTTPBasicAuth(qualys_api_username, qualys_api_password))

    if response.status_code == 200:
        root = ET.fromstring(response.text)
        try:
            if root.find(".//CODE").text == "SUCCESS":
                print('Report scan template created successfully!')
            else:
                print("Error creating report scan template.")
                print(f"Status code: {response.status_code}")
                message_element = root.find('.//MESSAGE')
                if message_element is not None:
                    print(f"Message: {message_element.text}")
                else:
                    print("Message element not found in the response. Response XML:")
                    print(response.text)
        except AttributeError:
            pass
    else:
        print(f'Error creating report scan template. Status code: {response.status_code}')
        print(response.text)

def create_dynamic_search_list(name, qualys_api_username, qualys_api_password):
    url = f"{QUALYS_BASE_URL}qid/search_list/dynamic/"

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Requested-With': 'Python Script',
    }

    data = {
        'action': 'create',
        'title': name,
        'global': '1',
        'confirmed_severities': '2,3,4,5',
        'potential_severities': '2,3,4,5'
    }

    response = requests.post(
        url,
        headers=headers,
        data=data,
        auth=HTTPBasicAuth(qualys_api_username, qualys_api_password)
    )

    if response.status_code == 200:
        xml_root = ET.fromstring(response.text)
        if xml_root.find('.//RESPONSE/CODE') is not None:
            error_code = xml_root.findtext('.//RESPONSE/CODE')
            error_msg = xml_root.findtext('.//RESPONSE/TEXT')
            print(f"Error creating search list: {error_code} - {error_msg}")
            return None
        else:
            search_list_id = xml_root.findtext('.//RESPONSE/ITEM_LIST/ITEM/VALUE')
            print(f"Created global template and dynamic search list '{name}' with ID {search_list_id}")
            return search_list_id
    else:
        print(f"Error creating search list: {response.status_code} - {response.text}")
        return None

if __name__ == "__main__":
    qualys_api_username = input("Enter your Qualys API username: ")
    qualys_api_password = getpass("Enter your Qualys API password: ")

    search_list_name = "zp general vulnerability sl"
    search_list_id = create_dynamic_search_list(search_list_name, qualys_api_username, qualys_api_password)

    if search_list_id:
        create_report_template(search_list_id, qualys_api_username, qualys_api_password)
