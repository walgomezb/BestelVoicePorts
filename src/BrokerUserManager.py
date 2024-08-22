import redis

class BrokerUserManager:
    def __init__(self, host='localhost', port=6379, db=0):
        self.r = redis.Redis(host=host, port=port, db=db)
        self.broker_id_key = 'broker:id'  # Key to store the next broker ID
        self.user_id_key = 'user:id'      # Key to store the next user ID

    def addBroker(self, brokerName):
        # Auto-increment broker ID
        brokerId = self.r.incr(self.broker_id_key)
        brokerKey = f'broker:{brokerId}'
        self.r.hset(brokerKey, mapping={'id': brokerId, 'name': brokerName})
        self.r.set(f'broker:name:{brokerName}', brokerId)
        return f"Broker {brokerName} added with ID {brokerId}."

    def updateBroker(self, brokerId, newBrokerName):
        brokerKey = f'broker:{brokerId}'
        if not self.r.exists(brokerKey):
            return f"Broker with ID {brokerId} does not exist."
        oldBrokerName = self.r.hget(brokerKey, 'name').decode('utf-8')
        self.r.hset(brokerKey, 'name', newBrokerName)
        self.r.delete(f'broker:name:{oldBrokerName}')
        self.r.set(f'broker:name:{newBrokerName}', brokerId)
        return f"Broker with ID {brokerId} updated to {newBrokerName}."

    def addUserByBrokerName(self, userName, brokerName, userPass):
        brokerId = self.r.get(f'broker:name:{brokerName}')
        if not brokerId:
            return f"Broker with name {brokerName} does not exist."
        brokerId = brokerId.decode('utf-8')
        return self._addUser(userName, brokerId, brokerName, userPass)

    def addUserByBrokerId(self, userName, brokerId, userPass):
        brokerKey = f'broker:{brokerId}'
        if not self.r.exists(brokerKey):
            return f"Broker with ID {brokerId} does not exist."
        brokerName = self.r.hget(brokerKey, 'name').decode('utf-8')
        return self._addUser(userName, brokerId, brokerName, userPass)

    def _addUser(self, userName, brokerId, brokerName, userPass):
        # Auto-increment user ID
        userId = self.r.incr(self.user_id_key)
        userKey = f'user:{userId}'
        self.r.hset(userKey, mapping={'id': userId, 'name': userName, 'broker_id': brokerId, 'pass': userPass})
        self.r.sadd(f'broker:{brokerId}:users', userId)
        self.r.set(f'user:name:{userName}', userId)
        return f"User {userName} added with ID {userId} to broker {brokerName}."

    def getBroker(self, brokerId):
        brokerKey = f'broker:{brokerId}'
        if not self.r.exists(brokerKey):
            return None
        broker = self.r.hgetall(brokerKey)
        return {k.decode('utf-8'): v.decode('utf-8') for k, v in broker.items()}

    def getUser(self, userId):
        userKey = f'user:{userId}'
        if not self.r.exists(userKey):
            return None
        user = self.r.hgetall(userKey)
        return {k.decode('utf-8'): v.decode('utf-8') for k, v in user.items()}

    def getUsersByBroker(self, brokerId):
        brokerKey = f'broker:{brokerId}'
        if not self.r.exists(brokerKey):
            return []
        userIds = self.r.smembers(f'broker:{brokerId}:users')
        users = []
        for userId in userIds:
            user = self.getUser(userId.decode('utf-8'))
            if user:
                users.append(user)
        return users

    def getBrokerByName(self, brokerName):
        brokerId = self.r.get(f'broker:name:{brokerName}')
        if not brokerId:
            return None
        return self.getBroker(brokerId.decode('utf-8'))

    def getUserByName(self, userName):
        userId = self.r.get(f'user:name:{userName}')
        if not userId:
            return None
        return self.getUser(userId.decode('utf-8'))

    def getAllUsers(self):
        userKeys = self.r.keys('user:*')
        users = []
        for userKey in userKeys:
            if userKey.decode('utf-8').startswith('user:') and userKey.decode('utf-8') != 'user:id':
                user = self.getUser(userKey.decode('utf-8').split(':')[1])
                if user:
                    users.append(user)
        return users

    def getAllBrokers(self):
        brokerIds = self.r.keys('broker:*')
        brokers = []
        for brokerId in brokerIds:
            if brokerId.decode('utf-8').startswith('broker:') and brokerId.decode('utf-8') != 'broker:id':
                broker = self.getBroker(brokerId.decode('utf-8').split(':')[1])
                if broker:
                    brokers.append(broker)
        return brokers
