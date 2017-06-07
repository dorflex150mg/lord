from controller.ClusterController import ClusterController
from controller.NodeController import NodeController
from loadbalancer.LoadBalancerManager import LoadBalancerManager
from util.IdGenerator import IdGenerator
from util.FileManager import FileManager
from util.urlManager import UrlManager

 

class ClusterCreator():
    idGenerator = None
    fileManager = None
    nodeController = None
    clusterController = None
    clusterCurrentPort = None
    haProxyManager = None
    urlManager = None
    clusterPort = 0
    serverPointer = 0
   
    
    def __init__(self, nodeController):
        self.idGenerator = IdGenerator()
        self.fileManager = FileManager()
        self.nodeController = nodeController
        self.clusterController = ClusterController()
        self.urlManager = UrlManager()
        self.clusterPort = 81 

    def createCluster(self, clusterController, cluster_name, dockerfile, instances, package, mem, port):
        cluster_id = self.idGenerator.getId()
        self.fileManager.set_dockerfile_path(cluster_id)
        self.fileManager.deploy_files(cluster_id, package, dockerfile_data)
        available_nodes = nodeController.getAvailableNodes()
        data = self.fileManager.getData(self.fileManager.getDockerfileDir(cluster_id))
        self.sendImageDataToNodes(availableNodes, cluster_id, cluster_name, dockerfile, data)
        clusterController.createCluster(cluster_id, cluster_name)
        LoadBalancerManager.addClusterFrontendToMain(self.clusterPort, cluster_id)
        self.createNetwork(cluster_id) 
        nodes_addresess = self.sendClusterParametersToNodes(instances, available_nodes, cluster_id, mem, port)
        LoadBalancerManager.addNodesAddressesToLoadBalancer(nodes_addresses)
        return True

    def sendImageDataToNodes(self, available_nodes, cluster_id, cluster_name, dockerfile, data):
        success = True
        for node in available_nodes:
            url = urlManager.assembleBuildURL(node.getIp())
            form_data = {'cluster_id': cluster_id, 'cluster_name': cluster_name, 'dockerfile': dockerfile, 'data': data)}
            datagen, headers = multipart_encode(form_data)
            request = urllib2.Request(url, datagen, headers)
            response = urllib2.urlopen(request)
            result = response.read()
            if not result:
                success = False
        return success

    def createNetwork(self, cluster_id):
        return True

    def sendClusterParametersToNodes(self, instances, available_nodes, cluster_id, mem, port):
        nodes_addresses = {}
        available_nodes_amount = len(available_nodes)
        for instance in range(instances):
            instance_address = self.sendInstanceParameterToNode(cluster_id, mem, port)
            nodes_addresses[instance_address['node_ip']] = instance_address['cluster_port_in_node']
        return nodes_addresses

    def addInstanceToCluster(self, cluster_id, mem, port):
        node_address_dict = self.sendInstanceParameterToNode(self, cluster_id, mem, port)
        node_address = {}
        node_address[node_address_dict['node_ip']] = node_address_dict['cluster_port_in_node']
        self.LoadBalancerManager.addNodesAddressesToLoadBalancer(node_address)

    def sendInstanceParamenterToNode(self, cluster_id, mem, port):
        node_ip = nodeManager.getNextNode().getIp()
        url = self.urlManager.assembleRunURL(node_ip)
        form_data = {'cluster_id' : cluster_id, 'mem' : mem, 'port' : port}
        params = urllib.urlencode(form_data)
        response = urllib2.urlopen(url, params)
        result = json.load(response)
        ips = result['result']
        cluster_port_in_node = ips['lb_port']
        return {'node_ip': node_ip, 'cluster_port_in_node': cluster_port_in_node}
        
