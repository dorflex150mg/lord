class LoadBalancer():
    loadBalancerId = None
    port = None
    instances = []

    def __init__(self, loadBalancerId, port):
        self.loadBalancerId = loadBalancerId
        self.port = port
    
    def getLoadBalancerId(self):
        return self.loadBalancerId

    def setLoadBalancerId(self, loadBalancerId):
        if loadBalancerId == None:
            raise TypeError("Id's must not be None")
        elif type(loadBalancerId) != str:
            raise TypeError("Id's must be of type string")
        elif loadBalancerId == "":
            raise ValueError("Id's must not be empty")
        else:
            self.loadBalancerId = loadBalancerId

    def getPort(self):
        return self.port

    def setPort(self, port):
        if port == None:
            raise TypeError("Load Balancer port must not be None")
        elif type(port) != str:
            raise TypeError("Load Balancer port must be of type string")
        elif port == "":
            raise ValueError("Load Balancer must not be empty")
        else:
            self.port = port

 
