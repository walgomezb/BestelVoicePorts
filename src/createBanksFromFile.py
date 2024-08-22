import pandas as pd
import requests

# Define the URL of the BankCentralRouterManager service
BANK_CENTRAL_ROUTER_MANAGER_URL = "http://localhost:9299/addBank"

# Define the path to the Excel file
EXCEL_FILE_PATH = "banks.xlsx"

def read_banks_from_excel(file_path):
    # Read the Excel file
    df = pd.read_excel(file_path)
    # Ensure the DataFrame has a column named 'bank_name'
    if 'bank_name' not in df.columns:
        raise ValueError("Excel file must contain a 'bank_name' column")
    return df['bank_name'].tolist()

def create_bank(bank_name):
    # Define the payload
    payload = {'bank_name': bank_name}
    # Make the HTTP POST request
    response = requests.post(BANK_CENTRAL_ROUTER_MANAGER_URL, json=payload)
    # Check the response status code
    if response.status_code == 200:
        print(f"Successfully created bank: {bank_name}")
    else:
        print(f"Failed to create bank: {bank_name}. Status code: {response.status_code}, Response: {response.text}")

def main():
    # Read banks from the Excel file
    banks = read_banks_from_excel(EXCEL_FILE_PATH)
    # Create each bank using the BankCentralRouterManager service
    for bank in banks:
        create_bank(bank)

if __name__ == "__main__":
    main()
