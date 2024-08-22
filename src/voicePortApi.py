from flask import Flask, request, jsonify
from BrokerUserManager import BrokerUserManager
from BankCentralRouterManager import BankCentralRouterManager

app = Flask(__name__)

broker_user_manager = BrokerUserManager()
bank_central_router_manager = BankCentralRouterManager()

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
    if not centralRouterName or not bankId:
        return jsonify({'error': 'central_router_name and bank_id are required'}), 400
    result = bank_central_router_manager.addCentralRouterByBankId(centralRouterName, bankId)
    return jsonify({'message': result})

@app.route('/addCentralRouterByBankName', methods=['POST'])
def addCentralRouterByBankName():
    data = request.json
    centralRouterName = data.get('central_router_name')
    bankName = data.get('bank_name')
    if not centralRouterName or not bankName:
        return jsonify({'error': 'central_router_name and bank_name are required'}), 400
    result = bank_central_router_manager.addCentralRouterByBankName(centralRouterName, bankName)
    return jsonify({'message': result})

@app.route('/updateCentralRouter', methods=['PUT'])
def updateCentralRouter():
    data = request.json
    centralRouterId = data.get('central_router_id')
    newCentralRouterName = data.get('new_central_router_name')
    if not centralRouterId or not newCentralRouterName:
        return jsonify({'error': 'central_router_id and new_central_router_name are required'}), 400
    result = bank_central_router_manager.updateCentralRouter(centralRouterId, newCentralRouterName)
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
    if not voicePortName or not centralRouterId or not brokerId or adminStatus is None or inputGain is None or outputAttenuation is None or operationalStatus is None:
        return jsonify({'error': 'voice_port_name, central_router_id, broker_id, admin_status, input_gain, output_attenuation, and operational_status are required'}), 400
    result = bank_central_router_manager.addVoicePortByCentralRouterId(voicePortName, centralRouterId, brokerId, adminStatus, inputGain, outputAttenuation, operationalStatus)
    return jsonify({'message': result})

@app.route('/updateVoicePort', methods=['PUT'])
def updateVoicePort():
    data = request.json
    voicePortId = data.get('voice_port_id')
    newVoicePortName = data.get('new_voice_port_name')
    brokerId = data.get('broker_id')
    adminStatus = data.get('admin_status')
    inputGain = data.get('input_gain')
    outputAttenuation = data.get('output_attenuation')
    operationalStatus = data.get('operational_status')
    if not voicePortId or not newVoicePortName or not brokerId or adminStatus is None or inputGain is None or outputAttenuation is None or operationalStatus is None:
        return jsonify({'error': 'voice_port_id, new_voice_port_name, broker_id, admin_status, input_gain, output_attenuation, and operational_status are required'}), 400
    result = bank_central_router_manager.updateVoicePort(voicePortId, newVoicePortName, brokerId, adminStatus, inputGain, outputAttenuation, operationalStatus)
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

@app.route('/getCentralRoutersByBank/<bankId>', methods=['GET'])
def getCentralRoutersByBank(bankId):
    result = bank_central_router_manager.getCentralRoutersByBank(bankId)
    return jsonify(result)

@app.route('/addBroker', methods=['POST'])
def addBroker():
    data = request.json
    brokerName = data.get('broker_name')
    if not brokerName:
        return jsonify({'error': 'broker_name is required'}), 400
    result = broker_user_manager.addBroker(brokerName)
    return jsonify({'message': result})

@app.route('/updateBroker', methods=['PUT'])
def updateBroker():
    data = request.json
    brokerId = data.get('broker_id')
    newBrokerName = data.get('new_broker_name')
    if not brokerId or not newBrokerName:
        return jsonify({'error': 'broker_id and new_broker_name are required'}), 400
    result = broker_user_manager.updateBroker(brokerId, newBrokerName)
    return jsonify({'message': result})

@app.route('/addUserByBrokerName', methods=['POST'])
def addUserByBrokerName():
    data = request.json
    userName = data.get('user_name')
    brokerName = data.get('broker_name')
    if not userName or not brokerName:
        return jsonify({'error': 'user_name and broker_name are required'}), 400
    result = broker_user_manager.addUserByBrokerName(userName, brokerName)
    return jsonify({'message': result})

@app.route('/addUserByBrokerId', methods=['POST'])
def addUserByBrokerId():
    data = request.json
    userName = data.get('user_name')
    brokerId = data.get('broker_id')
    if not userName or not brokerId:
        return jsonify({'error': 'user_name and broker_id are required'}), 400
    result = broker_user_manager.addUserByBrokerId(userName, brokerId)
    return jsonify({'message': result})

@app.route('/getBroker/<brokerId>', methods=['GET'])
def getBroker(brokerId):
    result = broker_user_manager.getBroker(brokerId)
    if result is None:
        return jsonify({'error': f'Broker with ID {brokerId} does not exist'}), 404
    return jsonify(result)

@app.route('/getUser/<userId>', methods=['GET'])
def getUser(userId):
    result = broker_user_manager.getUser(userId)
    if result is None:
        return jsonify({'error': f'User with ID {userId} does not exist'}), 404
    return jsonify(result)

@app.route('/getUsersByBroker/<brokerId>', methods=['GET'])
def getUsersByBroker(brokerId):
    result = broker_user_manager.getUsersByBroker(brokerId)
    return jsonify(result)

@app.route('/getBrokerByName/<brokerName>', methods=['GET'])
def getBrokerByName(brokerName):
    result = broker_user_manager.getBrokerByName(brokerName)
    if result is None:
        return jsonify({'error': f'Broker with name {brokerName} does not exist'}), 404
    return jsonify(result)

@app.route('/getUserByName/<userName>', methods=['GET'])
def getUserByName(userName):
    result = broker_user_manager.getUserByName(userName)
    if result is None:
        return jsonify({'error': f'User with name {userName} does not exist'}), 404
    return jsonify(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9099, debug=True)
