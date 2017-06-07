from Node import Node
from Instance import Instance
from sys import maxint

class Cluster():


    clusterId = None
    name = None
    instances = []
    nodes = []
    loadBalancers = []
    

    def __init__(self, clusterId, name):
       self.clusterId = clusterId 
       self.name = name

    def getClusterId(self):
        return self.clusterId

    def setClusterId(self, clusterId):
        if clusterId == None:
            raise TypeError("Id's must not be None")
        elif type(clusterId) != str:
            raise TypeError("Id's must be of type string")
        elif clusterId == "":
            raise ValueError("Id's must not be empty")
        else:
            self.clusterId = clusterId

    def getName(self):
        return self.name
 
    def setName(self, name):
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


    def addNode(self, node)
        if node is None:
            raise TypeError("Node must not be None")
        elif type(node) is not Instance:
            raise TypeError("Not a valid node")
        else:
            self.node.append(instance)

    def removeNode(self, nodeId):
        if nodeId is None:
            raise TypeError("Node must not be None")
        elif type(nodeId) is not str:
            raise TypeError("Not a valid node id")
        elif not self.nodes:
            raise IndexError("There are no nodes to remove from this cluster")
        node_index = 0
        for node in self.nodes:
            if node.getNodeId() == nodeId:
                del self.nodes[node_index]
                return True
            node_index += 1
        return False

    def addLoadBalancer(self, loadBalancer)
        if loadBalancer is None:
            raise TypeError("Load balancer must not be None")
        elif type(loadBalancer) is not LoadBalancer:
            raise TypeError("Not a valid load balancer")
        else:
            self.loadBalancers.append(loadBalancer)

    def removeLoadBalancer(self, loadBalancerId):
        if loadBalancerId is None:
            raise TypeError("Load balancer must not be None")
        elif type(loadBalancerId) is not str:
            raise TypeError("Not a valid load balancer id")
        elif not self.:
            raise IndexError("There are no load balancers to remove from this node")
        load_balancer_index = 0
        for load_balancer in self.loadBalancers:
            if loadBalancerId.getLoadBalancerId() == instanceId:
                del self.loadBalancers[load_balancer_index]
                return True
            load_balancer_index += 1
        return False

    def chooseNode():
        if not self.nodes:
            return False
        least_used_node = None
        least_node_amount = maxint()
        for node in self.nodes:
            if node.instancesAmount() < least_node_amount:
                least_used_node = node
                least_node_amount = node.instancesAmount()
        return least_used_node
        

 

         




          
