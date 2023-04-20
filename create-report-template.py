import requests
from requests.auth import HTTPBasicAuth
import xml.etree.ElementTree as ET

# Replace these with your Qualys API credentials
QUALYS_API_USERNAME = '#####'
QUALYS_API_PASSWORD = '#####'

# Update the base URL for the QG3 pod
QUALYS_BASE_URL = 'https://qualysguard.qg3.apps.qualys.com/api/2.0/fo/'

def create_scan_report_template(name, past_detections=2, asset_groups='all', cloud_agent_tag='All Cloud Agents'):
    url = f"{QUALYS_BASE_URL}report/template/scan/"

    headers = {
        'Content-Type': 'application/xml',
        'X-Requested-With': 'Python Script',  # Add a description for the X-Requested-With header
    }

    data = f"""
    <ServiceRequest>
        <data>
            <ReportTemplate>
                <name>{name}</name>
                <description></description>
                <type>Scan</type>
                <format>CSV</format>
                <action>create</action>
                <past_detections>{past_detections}</past_detections>
                <asset_groups>{asset_groups}</asset_groups>
                <cloud_agent_tag>{cloud_agent_tag}</cloud_agent_tag>
            </ReportTemplate>
        </data>
    </ServiceRequest>
    """

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
            print(f"Error creating scan report template: {error_code} - {error_msg}")
        else:
            template_id = xml_root.findtext('.//RESPONSE/ITEM_LIST/ITEM/VALUE')
            print(f"Created scan report template '{name}' with ID {template_id}")
    else:
        print(f"Error creating scan report template: {response.status_code} - {response.text}")

if __name__ == "__main__":
    report_template_name = "bv general vulnerability report"
    past_detections = 2
    asset_groups = "all"
    cloud_agent_tag = "All Cloud Agents"

    create_scan_report_template(report_template_name, past_detections, asset_groups, cloud_agent_tag)
