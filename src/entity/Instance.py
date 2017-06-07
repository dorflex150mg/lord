class Instance():
    instanceId = None
    name = None
    
    def __init__(self, instanceId, name):
        self.instanceId = instanceId
        self.name = instanceName

    def getInstanceId(self):
        return self.instanceId

    def setInstanceId(self, instanceId):
        if instanceId == None:
            raise TypeError("Id's must not be None")
        elif type(instanceId) != str:
            raise TypeError("Id's must of type string")
        elif instanceId == "":
            raise ValueError("Id's must not be empty")
        else:
             self.instanceId = instanceId

    def getName(self):
        return self.name()

    def setName(self, name):
        if name == None:
            raise TypeError("Name must not be None")
        elif type(nodeId) != str:
            raise TypeError("Name must be of type string")
        self.name = name
 
