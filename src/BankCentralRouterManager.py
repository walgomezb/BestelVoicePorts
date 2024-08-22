import redis
import requests, json


JOBRUNNER_HOST = "192.168.68.113"
JOBRUNNER_HOST = "jobrunner"


class BankCentralRouterManager:
    def __init__(self, host='localhost', port=6379, db=0):
        self.r = redis.Redis(host=host, port=port, db=db)
        self.bank_id_key = 'bank:id'  # Key to store the next bank ID
        self.central_router_id_key = 'central_router:id'  # Key to store the next central router ID
        self.voice_port_id_key = 'voice_port:id'  # Key to store the next voice port ID

    def addBank(self, bankName):
        # Auto-increment bank ID
        bankId = self.r.incr(self.bank_id_key)
        bankKey = f'bank:{bankId}'
        self.r.hset(bankKey, mapping={'id': bankId, 'name': bankName})
        self.r.set(f'bank:name:{bankName}', bankId)
        return f"Bank {bankName} added with ID {bankId}."

    def updateBank(self, bankId, newBankName):
        bankKey = f'bank:{bankId}'
        if not self.r.exists(bankKey):
            return f"Bank with ID {bankId} does not exist."
        oldBankName = self.r.hget(bankKey, 'name').decode('utf-8')
        self.r.hset(bankKey, 'name', newBankName)
        self.r.delete(f'bank:name:{oldBankName}')
        self.r.set(f'bank:name:{newBankName}', bankId)
        return f"Bank with ID {bankId} updated to {newBankName}."

    def addCentralRouterByBankId(self, centralRouterName, bankId, ip, model, brand, login, password):
        bankKey = f'bank:{bankId}'
        if not self.r.exists(bankKey):
            return f"Bank with ID {bankId} does not exist."
        # Auto-increment central router ID
        centralRouterId = self.r.incr(self.central_router_id_key)
        centralRouterKey = f'central_router:{centralRouterId}'
        self.r.hset(centralRouterKey, mapping={
            'id': centralRouterId,
            'name': centralRouterName,
            'bank_id': bankId,
            'ip': ip,
            'model': model,
            'brand': brand,
            'login': login,
            'pass': password
        })
        self.r.sadd(f'bank:{bankId}:central_routers', centralRouterId)
        self.r.set(f'central_router:name:{centralRouterName}', centralRouterId)
        return f"Central Router {centralRouterName} added with ID {centralRouterId} to bank {bankId}."

    def updateCentralRouter(self, centralRouterId, newCentralRouterName, ip, model, brand, login, password):
        centralRouterKey = f'central_router:{centralRouterId}'
        if not self.r.exists(centralRouterKey):
            return f"Central Router with ID {centralRouterId} does not exist."
        oldCentralRouterName = self.r.hget(centralRouterKey, 'name').decode('utf-8')
        self.r.hset(centralRouterKey, mapping={
            'name': newCentralRouterName,
            'ip': ip,
            'model': model,
            'brand': brand,
            'login': login,
            'pass': password
        })
        self.r.delete(f'central_router:name:{oldCentralRouterName}')
        self.r.set(f'central_router:name:{newCentralRouterName}', centralRouterId)
        return f"Central Router with ID {centralRouterId} updated to {newCentralRouterName}."

    def addCentralRouterByBankName(self, centralRouterName, bankName, ip, model, brand, login, password):
        bankId = self.r.get(f'bank:name:{bankName}')
        if not bankId:
            return f"Bank with name {bankName} does not exist."
        bankId = bankId.decode('utf-8')
        return self.addCentralRouterByBankId(centralRouterName, bankId, ip, model, brand, login, password)

    def addVoicePortByCentralRouterId(self, voicePortName, centralRouterId, brokerId, adminStatus, inputGain, outputAttenuation, operationalStatus, description):
        centralRouterKey = f'central_router:{centralRouterId}'
        if not self.r.exists(centralRouterKey):
            return f"Central Router with ID {centralRouterId} does not exist."
        # Auto-increment voice port ID
        voicePortId = self.r.incr(self.voice_port_id_key)
        voicePortKey = f'voice_port:{voicePortId}'
        self.r.hset(voicePortKey, mapping={
            'id': voicePortId,
            'name': voicePortName,
            'central_router_id': centralRouterId,
            'broker_id': brokerId,
            'admin_status': adminStatus,
            'input_gain': inputGain,
            'output_attenuation': outputAttenuation,
            'operational_status': operationalStatus,
            'description': description
        })
        self.r.sadd(f'central_router:{centralRouterId}:voice_ports', voicePortId)
        self.r.set(f'voice_port:name:{voicePortName}', voicePortId)
        return f"Voice Port {voicePortName} added with ID {voicePortId} to central router {centralRouterId}."

    def updateVoicePort(self, voicePortId, newVoicePortName, brokerId, adminStatus, inputGain, outputAttenuation, operationalStatus, description):
        voicePortKey = f'voice_port:{voicePortId}'
        if not self.r.exists(voicePortKey):
            return f"Voice Port with ID {voicePortId} does not exist."
        oldVoicePortName = self.r.hget(voicePortKey, 'name').decode('utf-8')
        self.r.hset(voicePortKey, mapping={
            'name': newVoicePortName,
            'broker_id': brokerId,
            'admin_status': adminStatus,
            'input_gain': inputGain,
            'output_attenuation': outputAttenuation,
            'operational_status': operationalStatus,
            'description': description
        })
        self.r.delete(f'voice_port:name:{oldVoicePortName}')
        self.r.set(f'voice_port:name:{newVoicePortName}', voicePortId)
        return f"Voice Port with ID {voicePortId} updated to {newVoicePortName}."

    def getBank(self, bankId):
        bankKey = f'bank:{bankId}'
        if not self.r.exists(bankKey):
            return None
        bank = self.r.hgetall(bankKey)
        return {k.decode('utf-8'): v.decode('utf-8') for k, v in bank.items()}

    def getBankByName(self, bankName):
        bankId = self.r.get(f'bank:name:{bankName}')
        if not bankId:
            return None
        return self.getBank(bankId.decode('utf-8'))

    def getAllBanks(self):
        bankIds = self.r.keys('bank:*')
        banks = []
        for bankId in bankIds:
            if bankId.decode('utf-8').startswith('bank:') and bankId.decode('utf-8') != 'bank:id':
                bank = self.getBank(bankId.decode('utf-8').split(':')[1])
                if bank:
                    banks.append(bank)
        return banks

    def getCentralRouter(self, centralRouterId):
        centralRouterKey = f'central_router:{centralRouterId}'
        if not self.r.exists(centralRouterKey):
            return None
        centralRouter = self.r.hgetall(centralRouterKey)
        return {k.decode('utf-8'): v.decode('utf-8') for k, v in centralRouter.items()}

    def getCentralRouterByName(self, centralRouterName):
        centralRouterId = self.r.get(f'central_router:name:{centralRouterName}')
        if not centralRouterId:
            return None
        return self.getCentralRouter(centralRouterId.decode('utf-8'))

    def getCentralRoutersByBankName(self, bankName):
        bankId = self.r.get(f"bank:name:{bankName}")
        if not bankId:
            return []
        bankId = bankId.decode("utf-8")
        centralRouterIds = self.r.smembers(f"bank:{bankId}:central_routers")
        centralRouters = []
        for centralRouterId in centralRouterIds:
            centralRouter = self.getCentralRouter(centralRouterId.decode("utf-8"))
            if centralRouter:
                centralRouters.append(centralRouter)
        return centralRouters

    def updateVoicePortFromRouter(self, centralRouterId):
        centralRouterKey = f"central_router:{centralRouterId}"
        if not self.r.exists(centralRouterKey):
            return f"Central Router with ID {centralRouterId} does not exist."
        # Remove all existing voice ports
        self.removeAllVoicePortsByCentralRouter(centralRouterId)

        centralRouter = self.r.hgetall(centralRouterKey)
        ip = centralRouter.get(b"ip").decode("utf-8")
        username = centralRouter.get(b"login").decode("utf-8")
        password = centralRouter.get(b"pass").decode("utf-8")
        password = "Onbo@rd1NG#0ToUcH2024"

        url = "http://"+JOBRUNNER_HOST+":9999/get_voice_ports"
        headers = {"Content-Type": "application/json"}
        payload = {"target_ip": ip, "username": username, "password": password}

        response = requests.post(url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            voicePorts = response.json()
            for voicePort in voicePorts:
                port = voicePort["port"]
                port = port.replace("/", "-")
                description = voicePort["description"]
                brokerId = None

                # Search for broker name in the description
                for brokerName in self.r.keys("broker:name:*"):
                    brokerName = brokerName.decode("utf-8").split(":")[-1]
                    if brokerName in description:
                        brokerId = self.r.get(f'broker:name:{brokerName}')
                        break

                if not brokerId:
                    brokerId = "unknown"  # Default value if broker name is not found
                    continue

                self.addVoicePortByCentralRouterId(
                    port,
                    centralRouterId,
                    brokerId,
                    voicePort["admin_status"],
                    voicePort["input_gain"],
                    voicePort["output_attenuation"],
                    voicePort["oper"], description
                )

            return f"Voice ports updated for central router with ID {centralRouterId}."
        else:
            return f"Failed to update voice ports for central router with ID {centralRouterId}. Status code: {response.status_code}, Response: {response.text}"

    def saveVoicePortToRouter(self, centralRouterId, voicePortId, input_gain, output_attenuation, port_name, admin_status, broker_id, description):

        centralRouterKey = f"central_router:{centralRouterId}"
        if not self.r.exists(centralRouterKey):
            return f"Central Router with ID {centralRouterId} does not exist."

        centralRouter = self.r.hgetall(centralRouterKey)
        ip = centralRouter.get(b"ip").decode("utf-8")
        username = centralRouter.get(b"login").decode("utf-8")
        password = centralRouter.get(b"pass").decode("utf-8")
        password = "Onbo@rd1NG#0ToUcH2024"
        port_name = port_name.replace("-","/")

        if (admin_status=="down"):
            admin_status="shutdown"
        else:
            admin_status="no shutdown"

        
        url = "http://" + JOBRUNNER_HOST + ":9999/writeVoicePortConfig"
        headers = {"Content-Type": "application/json"}
        payload = {
            "target_ip": ip,
            "username": username,
            "password": password,
            "port_name": port_name,
            "input_gain": input_gain,
            "output_attenuation": output_attenuation,
            "admin_status": admin_status,
        }

        response = requests.post(url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            port_name = port_name.replace("/","-")
            self.updateVoicePort(voicePortId, port_name, broker_id, admin_status, input_gain, output_attenuation, "", description)
            return f"Voice port {port_name} updated for central router with ID {centralRouterId}."
        else:
            return f"Failed to update voice port {port_name} for central router with ID {centralRouterId}. Status code: {response.status_code}, Response: {response.text}"

    def getVoicePort(self, voicePortId):
        voicePortKey = f"voice_port:{voicePortId}"
        if not self.r.exists(voicePortKey):
            return None
        voicePort = self.r.hgetall(voicePortKey)
        return {k.decode("utf-8"): v.decode("utf-8") for k, v in voicePort.items()}

    def getVoicePortByName(self, voicePortName):
        voicePortId = self.r.get(f"voice_port:name:{voicePortName}")
        if not voicePortId:
            return None
        return self.getVoicePort(voicePortId.decode("utf-8"))

    def getVoicePortsByCentralRouter(self, centralRouterId):
        centralRouterKey = f"central_router:{centralRouterId}"
        if not self.r.exists(centralRouterKey):
            return []
        voicePortIds = self.r.smembers(f"central_router:{centralRouterId}:voice_ports")
        voicePorts = []
        for voicePortId in voicePortIds:
            voicePort = self.getVoicePort(voicePortId.decode("utf-8"))
            if voicePort:
                voicePorts.append(voicePort)
        return voicePorts

    def getVoicePortsByCentralRouterAndBroker(self, centralRouterId, brokerId):
        centralRouterKey = f"central_router:{centralRouterId}"
        if not self.r.exists(centralRouterKey):
            return []
        voicePortIds = self.r.smembers(f"central_router:{centralRouterId}:voice_ports")
        voicePorts = []
        for voicePortId in voicePortIds:
            voicePort = self.getVoicePort(voicePortId.decode("utf-8"))
            if voicePort and str(voicePort.get("broker_id")) == str(brokerId):
                voicePorts.append(voicePort)
        return voicePorts

    def removeAllVoicePortsByCentralRouter(self, centralRouterId):
        centralRouterKey = f"central_router:{centralRouterId}"
        if not self.r.exists(centralRouterKey):
            return f"Central Router with ID {centralRouterId} does not exist."
        voicePortIds = self.r.smembers(f"central_router:{centralRouterId}:voice_ports")
        for voicePortId in voicePortIds:
            voicePortKey = f'voice_port:{voicePortId.decode("utf-8")}'
            self.r.delete(voicePortKey)
        self.r.delete(f"central_router:{centralRouterId}:voice_ports")
        return f"All voice ports removed from central router with ID {centralRouterId}."

    def getVoicePortsByBank(self, bankId):
        centralRouters = self.getCentralRoutersByBank(bankId)
        all_voice_ports = []
        for centralRouter in centralRouters:
            voicePorts = self.getVoicePortsByCentralRouter(centralRouter["id"])
            all_voice_ports.extend(voicePorts)
        return all_voice_ports

    def getCentralRoutersByBank(self, bankId):
        bankKey = f"bank:{bankId}"
        if not self.r.exists(bankKey):
            return []
        centralRouterIds = self.r.smembers(f"bank:{bankId}:central_routers")
        centralRouters = []
        for centralRouterId in centralRouterIds:
            centralRouter = self.getCentralRouter(centralRouterId.decode("utf-8"))
            if centralRouter:
                centralRouters.append(centralRouter)
        return centralRouters
