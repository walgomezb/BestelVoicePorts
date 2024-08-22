import pandas as pd
import requests

# Define the URL of the BankCentralRouterManager service
BANK_CENTRAL_ROUTER_MANAGER_URL = "http://127.0.0.1:9299/addCentralRouterByBankName"

# Define the path to the Excel file
EXCEL_FILE_PATH = "central_routers.xlsx"

def read_central_routers_from_excel(file_path):
    # Read the Excel file
    df = pd.read_excel(file_path)
    # Ensure the DataFrame has the required columns
    required_columns = {'central_router_name', 'bank_name', 'ip', 'model', 'brand', 'login', 'pass'}
    if not required_columns.issubset(df.columns):
        raise ValueError(f"Excel file must contain the following columns: {required_columns}")
    return df.to_dict(orient='records')

def create_central_router(central_router):
    # Define the payload
    payload = {
        'central_router_name': central_router['central_router_name'],
        'bank_name': central_router['bank_name'],
        'ip': central_router['ip'],
        'model': central_router['model'],
        'brand': central_router['brand'],
        'login': central_router['login'],
        'pass': central_router['pass']
    }
    # Make the HTTP POST request
    response = requests.post(BANK_CENTRAL_ROUTER_MANAGER_URL, json=payload)
    # Check the response status code
    if response.status_code == 200:
        print(f"Successfully created central router: {central_router['central_router_name']} for bank: {central_router['bank_name']}")
    else:
        print(f"Failed to create central router: {central_router['central_router_name']} for bank: {central_router['bank_name']}. Status code: {response.status_code}, Response: {response.text}")

def main():
    # Read central routers from the Excel file
    central_routers = read_central_routers_from_excel(EXCEL_FILE_PATH)
    # Create each central router using the BankCentralRouterManager service
    for central_router in central_routers:
        create_central_router(central_router)

if __name__ == "__main__":
    main()
