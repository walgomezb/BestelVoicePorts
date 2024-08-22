import pandas as pd
import requests

# Define the URL of the BrokerUserManager service
BROKER_USER_MANAGER_URL = "http://localhost:9099/addBroker"

# Define the path to the Excel file
EXCEL_FILE_PATH = "./brokers.xlsx"

def read_brokers_from_excel(file_path):
    # Read the Excel file
    df = pd.read_excel(file_path)
    # Ensure the DataFrame has a column named 'broker_name'
    if 'broker_name' not in df.columns:
        raise ValueError("Excel file must contain a 'broker_name' column")
    return df['broker_name'].tolist()

def create_broker(broker_name):
    # Define the payload
    payload = {'broker_name': broker_name}
    # Make the HTTP POST request
    response = requests.post(BROKER_USER_MANAGER_URL, json=payload)
    # Check the response status code
    if response.status_code == 200:
        print(f"Successfully created broker: {broker_name}")
    else:
        print(f"Failed to create broker: {broker_name}. Status code: {response.status_code}, Response: {response.text}")

def main():
    # Read brokers from the Excel file
    brokers = read_brokers_from_excel(EXCEL_FILE_PATH)
    # Create each broker using the BrokerUserManager service
    for broker in brokers:
        create_broker(broker)

if __name__ == "__main__":
    main()
