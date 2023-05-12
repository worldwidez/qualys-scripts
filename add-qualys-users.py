import csv
import requests
from xml.etree import ElementTree
import getpass

QUALYS_API_BASE_URL = "https://qualysapi.qg3.apps.qualys.com/msp/user.php"
API_USERNAME = input("Enter your API username: ")
API_PASSWORD = getpass.getpass("Enter your API password: ")

def create_qualys_user(user_role, first_name, last_name, email, business_unit, phone, title, address1, city, country, state, zip_code, send_email=0):
    # Prepare user data
    user_data = {
        "action": "add",
        "user_role": user_role,
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "business_unit": business_unit,
        "phone": phone,
        "title": title,
        "address1": address1,
        "city": city,
        "country": country,
        "state": state,
        "zip_code": zip_code,
        "send_email": send_email
    }

    # Send POST request to Qualys API
    response = requests.post(
        QUALYS_API_BASE_URL,
        auth=(API_USERNAME, API_PASSWORD),
        data=user_data,
    )

    # Check for successful request
    if response.status_code == 200:
        print(f"User {first_name} {last_name} created successfully!")

        # Parse the XML response to extract the username and password
        tree = ElementTree.fromstring(response.content)
        username_element = tree.find(".//USER_LOGIN")
        password_element = tree.find(".//PASSWORD")

        if username_element is not None and password_element is not None:
            username = username_element.text
            password = password_element.text
            return (username, password)
        else:
            print("Failed to extract username and password from the XML response.")
            return None
    else:
        print(f"Failed to create user: {response.text}")
        return None

def process_csv_file(csv_file_path):
    created_users = []

    with open(csv_file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            user_role = row['user_role']
            first_name = row['first_name']
            last_name = row['last_name']
            email = row['email']
            business_unit = row['business_unit']
            phone = row['phone']
            title = row['title']
            address1 = row['address1']
            city = row['city']
            country = row['country']
            state = row['state']
            zip_code = row['zip_code']

            result = create_qualys_user(user_role, first_name, last_name, email, business_unit, phone, title, address1, city, country, state, zip_code)
            if result:
                username, password = result
                created_users.append({
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "username": username,
                    "password": password
                })

    # Write the created users' information to a new CSV file
    with open("created_users.csv", mode="w", newline='') as csvfile:
        fieldnames = ["first_name", "last_name", "email", "username", "password"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for user in created_users:
            writer.writerow(user)


# Example usage
csv_file_path = "users.csv"  # Replace with the path to your CSV file
process_csv_file(csv_file_path)
