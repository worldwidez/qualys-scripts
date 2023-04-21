import requests
from requests.auth import HTTPBasicAuth
import xml.etree.ElementTree as ET

# Replace these with your Qualys API credentials
username = '#####'
password = '#####'

# Update the base URL for the QG3 pod
QUALYS_BASE_URL = 'https://qualysguard.###.apps.qualys.com/api/2.0/fo/report/template/scan/'

# Add the action and report_format parameters to the URL
url = QUALYS_BASE_URL + "?action=create&report_format=csv"

# Set the headers
headers = {
    'Content-Type': 'application/xml',
    'X-Requested-With': 'Python requests'
}

# Define the XML payload for creating the report scan template
xml_payload = """
<REPORT_TEMPLATE>
  <TITLE>Api Created Report Scan Template</TITLE>
  <TEMPLATE_TYPE>Scan</TEMPLATE_TYPE>
  <OUTPUT_FORMAT>csv</OUTPUT_FORMAT>
  <REPORT_DETAILS>
    <DISPLAY>Default</DISPLAY>
    <FILTER>
      <SEVERITY>
        <CONFIRMED>2-5</CONFIRMED>
        <POTENTIAL>2-5</POTENTIAL>
      </SEVERITY>
      <DETECTION>
        <NEW_PREV>2</NEW_PREV>
      </DETECTION>
    </FILTER>
    <ASSET_GROUPS>all</ASSET_GROUPS>
    <CLOUD_AGENTS>all</CLOUD_AGENTS>
    <AGENT_DATA>true</AGENT_DATA>
    <SCAN_DATA>true</SCAN_DATA>
    <DETAILED_RESULTS>
      <TEXT_SUMMARY>true</TEXT_SUMMARY>
      <VULNERABILITY_DETAILS>true</VULNERABILITY_DETAILS>
      <THREAT>true</THREAT>
      <IMPACT>true</IMPACT>
      <SOLUTION>true</SOLUTION>
      <PATCHES_AND_WORKAROUNDS>true</PATCHES_AND_WORKAROUNDS>
      <VIRTUAL_PATCHES>true</VIRTUAL_PATCHES>
      <MITIGATING_CONTROLS>true</MITIGATING_CONTROLS>
      <COMPLIANCE>true</COMPLIANCE>
      <EXPLOITABILITY>true</EXPLOITABILITY>
      <ASSOCIATED_MALWARE>true</ASSOCIATED_MALWARE>
      <RESULTS>true</RESULTS>
      <REOPENED>true</REOPENED>
    </DETAILED_RESULTS>
  </REPORT_DETAILS>
  <TARGET>
    <HOST_BASED>true</HOST_BASED>
  </TARGET>
</REPORT_TEMPLATE>
"""

# Make the API request
response = requests.post(url, headers=headers, data=xml_payload, auth=HTTPBasicAuth(username, password))

# Check the response status
if response.status_code == 200:
    print('Report scan template created successfully!')
else:
    print(f'Error creating report scan template. Status code: {response.status_code}')
    print(response.text)
