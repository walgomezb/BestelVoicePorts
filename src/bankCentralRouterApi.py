from flask import Flask, request, jsonify
from BankCentralRouterManager import BankCentralRouterManager
from flask_cors import CORS


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

bank_central_router_manager = BankCentralRouterManager(host="redis")

@app.route('/addBank', methods=['POST'])
def addBank():
    data = request.json
    bankName = data.get('bank_name')
    if not bankName:
        return jsonify({'error': 'bank_name is required'}), 400
    result = bank_central_router_manager.addBank(bankName)
    return jsonify({'message': result})

@app.route('/updateBank', methods=['PUT'])
def updateBank():
    data = request.json
    bankId = data.get('bank_id')
    newBankName = data.get('new_bank_name')
    if not bankId or not newBankName:
        return jsonify({'error': 'bank_id and new_bank_name are required'}), 400
    result = bank_central_router_manager.updateBank(bankId, newBankName)
    return jsonify({'message': result})

@app.route('/addCentralRouterByBankId', methods=['POST'])
def addCentralRouterByBankId():
    data = request.json
    centralRouterName = data.get('central_router_name')
    bankId = data.get('bank_id')
    ip = data.get('ip')
    model = data.get('model')
    brand = data.get('brand')
    login = data.get('login')
    password = data.get('pass')
    if not centralRouterName or not bankId or not ip or not model or not brand or not login or not password:
        return jsonify({'error': 'central_router_name, bank_id, ip, model, brand, login, and pass are required'}), 400
    result = bank_central_router_manager.addCentralRouterByBankId(centralRouterName, bankId, ip, model, brand, login, password)
    return jsonify({'message': result})

@app.route('/addCentralRouterByBankName', methods=['POST'])
def addCentralRouterByBankName():
    data = request.json
    centralRouterName = data.get('central_router_name')
    bankName = data.get('bank_name')
    ip = data.get('ip')
    model = data.get('model')
    brand = data.get('brand')
    login = data.get('login')
    password = data.get('pass')
    if not centralRouterName or not bankName or not ip or not model or not brand or not login or not password:
        return jsonify({'error': 'central_router_name, bank_name, ip, model, brand, login, and pass are required'}), 400
    result = bank_central_router_manager.addCentralRouterByBankName(centralRouterName, bankName, ip, model, brand, login, password)
    return jsonify({'message': result})

@app.route('/updateCentralRouter', methods=['PUT'])
def updateCentralRouter():
    data = request.json
    centralRouterId = data.get('central_router_id')
    newCentralRouterName = data.get('new_central_router_name')
    ip = data.get('ip')
    model = data.get('model')
    brand = data.get('brand')
    login = data.get('login')
    password = data.get('pass')
    if not centralRouterId or not newCentralRouterName or not ip or not model or not brand or not login or not password:
        return jsonify({'error': 'central_router_id, new_central_router_name, ip, model, brand, login, and pass are required'}), 400
    result = bank_central_router_manager.updateCentralRouter(centralRouterId, newCentralRouterName, ip, model, brand, login, password)
    return jsonify({'message': result})

@app.route('/addVoicePortByCentralRouterId', methods=['POST'])
def addVoicePortByCentralRouterId():
    data = request.json
    voicePortName = data.get('voice_port_name')
    centralRouterId = data.get('central_router_id')
    brokerId = data.get('broker_id')
    adminStatus = data.get('admin_status')
    inputGain = data.get('input_gain')
    outputAttenuation = data.get('output_attenuation')
    operationalStatus = data.get('operational_status')
    description = data.get('description')
    if not voicePortName or not centralRouterId or not brokerId or adminStatus is None or inputGain is None or outputAttenuation is None or operationalStatus is None or description is None:
        return jsonify({'error': 'voice_port_name, central_router_id, broker_id, admin_status, input_gain, output_attenuation, operational_status, and description are required'}), 400
    result = bank_central_router_manager.addVoicePortByCentralRouterId(voicePortName, centralRouterId, brokerId, adminStatus, inputGain, outputAttenuation, operationalStatus, description)
    return jsonify({'message': result})

@app.route('/updateVoicePort', methods=['PUT'])
def updateVoicePort():
    data = request.json
    voicePortId = data.get('voice_port_id')
    newVoicePortName = data.get('voice_port_name')
    brokerId = data.get('broker_id')
    adminStatus = data.get('admin_status')
    inputGain = data.get('input_gain')
    outputAttenuation = data.get('output_attenuation')
    operationalStatus = data.get('operational_status')
    description = data.get('description')
    if not voicePortId or not newVoicePortName or not brokerId or adminStatus is None or inputGain is None or outputAttenuation is None or operationalStatus is None or description is None:
        return jsonify({'error': 'voice_port_id, new_voice_port_name, broker_id, admin_status, input_gain, output_attenuation, operational_status, and description are required'}), 400
    result = bank_central_router_manager.updateVoicePort(voicePortId, newVoicePortName, brokerId, adminStatus, inputGain, outputAttenuation, operationalStatus, description)
    return jsonify({'message': result})

@app.route('/getBank/<bankId>', methods=['GET'])
def getBank(bankId):
    result = bank_central_router_manager.getBank(bankId)
    if result is None:
        return jsonify({'error': f'Bank with ID {bankId} does not exist'}), 404
    return jsonify(result)

@app.route('/getBankByName/<bankName>', methods=['GET'])
def getBankByName(bankName):
    result = bank_central_router_manager.getBankByName(bankName)
    if result is None:
        return jsonify({'error': f'Bank with name {bankName} does not exist'}), 404
    return jsonify(result)

@app.route('/getAllBanks', methods=['GET'])
def getAllBanks():
    result = bank_central_router_manager.getAllBanks()
    return jsonify(result)

@app.route('/getCentralRouter/<centralRouterId>', methods=['GET'])
def getCentralRouter(centralRouterId):
    result = bank_central_router_manager.getCentralRouter(centralRouterId)
    if result is None:
        return jsonify({'error': f'Central Router with ID {centralRouterId} does not exist'}), 404
    return jsonify(result)

@app.route('/getCentralRouterByName/<centralRouterName>', methods=['GET'])
def getCentralRouterByName(centralRouterName):
    result = bank_central_router_manager.getCentralRouterByName(centralRouterName)
    if result is None:
        return jsonify({'error': f'Central Router with name {centralRouterName} does not exist'}), 404
    return jsonify(result)

@app.route('/getCentralRoutersByBankName/<bankName>', methods=['GET'])
def getCentralRoutersByBankName(bankName):
    result = bank_central_router_manager.getCentralRoutersByBankName(bankName)
    return jsonify(result)

@app.route('/getVoicePort/<voicePortId>', methods=['GET'])
def getVoicePort(voicePortId):
    result = bank_central_router_manager.getVoicePort(voicePortId)
    if result is None:
        return jsonify({'error': f'Voice Port with ID {voicePortId} does not exist'}), 404
    return jsonify(result)

@app.route('/getVoicePortByName/<voicePortName>', methods=['GET'])
def getVoicePortByName(voicePortName):
    result = bank_central_router_manager.getVoicePortByName(voicePortName)
    if result is None:
        return jsonify({'error': f'Voice Port with name {voicePortName} does not exist'}), 404
    return jsonify(result)

@app.route('/getVoicePortsByCentralRouter/<centralRouterId>', methods=['GET'])
def getVoicePortsByCentralRouter(centralRouterId):
    result = bank_central_router_manager.getVoicePortsByCentralRouter(centralRouterId)
    return jsonify(result)

@app.route('/getVoicePortsByCentralRouterAndBroker/<centralRouterId>/<brokerId>', methods=['GET'])
def getVoicePortsByCentralRouterAndBroker(centralRouterId, brokerId):
    result = bank_central_router_manager.getVoicePortsByCentralRouterAndBroker(centralRouterId, brokerId)
    return jsonify(result)

@app.route('/removeAllVoicePortsByCentralRouter/<centralRouterId>', methods=['DELETE'])
def removeAllVoicePortsByCentralRouter(centralRouterId):
    result = bank_central_router_manager.removeAllVoicePortsByCentralRouter(centralRouterId)
    return jsonify({'message': result})

@app.route('/getVoicePortsByBank/<bankId>', methods=['GET'])
def getVoicePortsByBank(bankId):
    result = bank_central_router_manager.getVoicePortsByBank(bankId)
    return jsonify(result)

@app.route('/getCentralRoutersByBank/<bankId>', methods=['GET'])
def getCentralRoutersByBank(bankId):
    result = bank_central_router_manager.getCentralRoutersByBank(bankId)
    return jsonify(result)

@app.route('/updateVoicePortFromRouter/<centralRouterId>', methods=['POST'])
def updateVoicePortFromRouter(centralRouterId):
    result = bank_central_router_manager.updateVoicePortFromRouter(centralRouterId)
    return jsonify({'message': result})


@app.route('/saveVoicePortToRouter', methods=['POST'])
def saveVoicePortToRouter():
    data = request.json
    centralRouterId = data.get('central_router_id')
    voicePortId = data.get('voice_port_id')
    input_gain = data.get('input_gain')
    output_attenuation = data.get('output_attenuation')
    port_name = data.get('port_name')
    admin_status = data.get('admin_status')
    broker_id = data.get('broker_id')
    description = data.get('description')
    result = bank_central_router_manager.saveVoicePortToRouter(centralRouterId, voicePortId, input_gain, output_attenuation, port_name, admin_status, broker_id, description)
    return jsonify({'message': result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9299, debug=True)
