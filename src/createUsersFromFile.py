import pandas as pd
import requests

# Define the URL of the BrokerUserManager service
BROKER_USER_MANAGER_URL = "http://localhost:9099/addUserByBrokerName"

# Define the path to the Excel file
EXCEL_FILE_PATH = "users.xlsx"

def read_users_from_excel(file_path):
    # Read the Excel file
    df = pd.read_excel(file_path)
    # Ensure the DataFrame has the required columns
    required_columns = {'user_name', 'broker_name', 'pass'}
    if not required_columns.issubset(df.columns):
        raise ValueError(f"Excel file must contain the following columns: {required_columns}")
    return df.to_dict(orient='records')

def create_user(user):
    # Define the payload
    payload = {
        'user_name': user['user_name'],
        'broker_name': user['broker_name'],
        'pass': user['pass']
    }
    # Make the HTTP POST request
    response = requests.post(BROKER_USER_MANAGER_URL, json=payload)
    # Check the response status code
    if response.status_code == 200:
        print(f"Successfully created user: {user['user_name']} for broker: {user['broker_name']}")
    else:
        print(f"Failed to create user: {user['user_name']} for broker: {user['broker_name']}. Status code: {response.status_code}, Response: {response.text}")

def main():
    # Read users from the Excel file
    users = read_users_from_excel(EXCEL_FILE_PATH)
    # Create each user using the BrokerUserManager service
    for user in users:
        create_user(user)

if __name__ == "__main__":
    main()
