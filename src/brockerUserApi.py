from flask import Flask, request, jsonify
from BrokerUserManager import BrokerUserManager
from flask_cors import CORS


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
broker_user_manager = BrokerUserManager(host="redis")

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
    userPass = data.get('pass')
    if not userName or not brokerName or not userPass:
        return jsonify({'error': 'user_name, broker_name, and pass are required'}), 400
    result = broker_user_manager.addUserByBrokerName(userName, brokerName, userPass)
    return jsonify({'message': result})

@app.route('/addUserByBrokerId', methods=['POST'])
def addUserByBrokerId():
    data = request.json
    userName = data.get('user_name')
    brokerId = data.get('broker_id')
    userPass = data.get('pass')
    if not userName or not brokerId or not userPass:
        return jsonify({'error': 'user_name, broker_id, and pass are required'}), 400
    result = broker_user_manager.addUserByBrokerId(userName, brokerId, userPass)
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

@app.route('/getAllBrokers', methods=['GET'])
def getAllBrokers():
    result = broker_user_manager.getAllBrokers()
    return jsonify(result)

@app.route('/getAllUsers', methods=['GET'])
def getAllUsers():
    result = broker_user_manager.getAllUsers()
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9099, debug=True)
