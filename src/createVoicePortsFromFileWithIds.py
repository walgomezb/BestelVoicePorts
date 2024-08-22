import pandas as pd
import requests
from urllib.parse import quote

# Define the URLs of the BankCentralRouterManager and BrokerUserManager services
BANK_CENTRAL_ROUTER_MANAGER_URL = "http://127.0.0.1:9299"
BROKER_USER_MANAGER_URL = "http://127.0.0.1:9099"

# Define the path to the Excel file
EXCEL_FILE_PATH = "src/voice_ports.xlsx"

def read_voice_ports_from_excel(file_path):
    # Read the Excel file
    df = pd.read_excel(file_path)
    # Ensure the DataFrame has the required columns
    required_columns = {'voice_port_name', 'central_router_id', 'broker_name', 'admin_status', 'input_gain', 'output_attenuation', 'operational_status', 'description'}
    if not required_columns.issubset(df.columns):
        raise ValueError(f"Excel file must contain the following columns: {required_columns}")
    return df.to_dict(orient='records')

def get_broker_id_by_name(broker_name):
    response = requests.get(f"{BROKER_USER_MANAGER_URL}/getBrokerByName/{quote(broker_name)}", headers={'Content-Type': 'application/json; charset=utf-8'})
    if response.status_code == 200:
        broker = response.json()
        return broker['id']
    else:
        raise ValueError(f"Broker with name {broker_name} does not exist. Status code: {response.status_code}, Response: {response.text}")

def get_voice_port_by_name_and_central_router(voice_port_name, central_router_id):
    
    response = requests.get(f"{BANK_CENTRAL_ROUTER_MANAGER_URL}/getVoicePortByName/{quote(voice_port_name)}", headers={'Content-Type': 'application/json; charset=utf-8'})
    if response.status_code == 200:
        voice_port = response.json()
        if voice_port['central_router_id'] == str(central_router_id):
            return voice_port
    return None

def create_or_update_voice_port(voice_port):
    # Resolve Broker name to ID
    broker_id = get_broker_id_by_name(voice_port['broker_name'])
    # Check if the voice port already exists
    existing_voice_port = get_voice_port_by_name_and_central_router(voice_port['voice_port_name'], voice_port['central_router_id'])
    # Define the payload
    payload = {
        'voice_port_name': voice_port['voice_port_name'],
        'central_router_id': voice_port['central_router_id'],
        'broker_id': broker_id,
        'admin_status': voice_port['admin_status'],
        'input_gain': voice_port['input_gain'],
        'output_attenuation': voice_port['output_attenuation'],
        'operational_status': voice_port['operational_status'],
        'description': voice_port['description']
    }
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    if existing_voice_port:
        # Update the existing voice port
        payload['voice_port_id'] = existing_voice_port['id']
        response = requests.put(f"{BANK_CENTRAL_ROUTER_MANAGER_URL}/updateVoicePort", json=payload, headers=headers)
        action = "updated"
    else:
        # Create a new voice port
        response = requests.post(f"{BANK_CENTRAL_ROUTER_MANAGER_URL}/addVoicePortByCentralRouterId", json=payload, headers=headers)
        action = "created"
    # Check the response status code
    if response.status_code == 200:
        print(f"Successfully {action} voice port: {voice_port['voice_port_name']} for central router ID: {voice_port['central_router_id']}")
    else:
        print(f"Failed to {action} voice port: {voice_port['voice_port_name']} for central router ID: {voice_port['central_router_id']}. Status code: {response.status_code}, Response: {response.text}")

def main():
    # Read voice ports from the Excel file
    voice_ports = read_voice_ports_from_excel(EXCEL_FILE_PATH)
    # Create or update each voice port using the BankCentralRouterManager service
    for voice_port in voice_ports:
        create_or_update_voice_port(voice_port)

if __name__ == "__main__":
    main()
