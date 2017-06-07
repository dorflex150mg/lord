class Node():
    nodeId = None
    name = None
    ip = None
    instances = []

    def __init__(self, nodeId, name, ip):
        self.nodeId = nodeId
        self.name = name
        self.ip = ip

    def getNodeId(self):
        return self.nodeId

    def setNodeId(self, nodeId):
        if nodeId == None:
            raise TypeError("Id's must not be None")
        elif type(nodeId) != str:
            raise TypeError("Id's must of type string")
        elif nodeId == "":
            raise ValueError("Id's must not be empty")
        else:
            self.nodeId = nodeId

    def getNodeName(self):
        return self.name

    def setNodeName(self, name):
        if name == None:
            raise TypeError("Name must not be None")
        elif type(nodeId) != str:
            raise TypeError("Name must be of type string")
        self.name = name


    def addInstance(self, instance)
        if instance is None:
            raise TypeError("Instance must not be None")
        elif type(instance) is not Instance:
            raise TypeError("Not a valid instance")
        else:
            self.instances.append(instance)

    def removeInstance(self, instanceId):
        if instanceId is None:
            raise TypeError("Instance must not be None")
        elif type(instanceId) is not str:
            raise TypeError("Not a valid instance id")
        elif not self.instances:
            raise IndexError("There are no instances to remove from this node")
        instance_index = 0
        for instance in self.instances:
            if instance.getInstanceId() == instanceId:
                del instance[instance_index]
                return True
            instance_index += 1
        return False

