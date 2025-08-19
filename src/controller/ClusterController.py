class ClusterController():
  clusters = []

#  def __init__(self):

  def createCluster(self, cluster_id, name):
      if self.clusters:
          for cluster in self.clusters:
              if cluster.getClusterId() == cluster_id:
                  raise ValueError("Cluster id already exists. Choose another")
              elif cluster.getName() == name:
                  raise ValueError("Cluster name already exists. Choose another")
       new_cluster = Cluster(cluster_id, name)
       if addClusterToEngine(cluster_id)
           self.clusters.append(new_cluster)


  def removeClusterByName(self, name):
      if not clusters:
          raise IndexError("There are no clusters to be removed")
      else:
          cluster_index = 0
          for cluster in self.clusters:
              if cluster.getName() == name:
                   if removeClusterFromEngine():
                       del self.clusters[cluster_index]
              clusert_index += 1 


  def addInstanceToCluster(self, instance, cluster_id):
      if not clusters:
          raise IndexError("There are no clusters created")
      for cluster in clusters:
          if cluster.getClusterId() == cluster_id:
              choosenNode = cluster.chooseNode()
              if choosenNode:
                 choosenNode.addInstance(instance)
                 cluster.addInstance(instance)
                 return True
      return False

  def removeInstanceFromCluster(self, instance, cluster_id):
      if not clusters:
          raise IndexError("There are no clusters created")
      cluster_index = 0
      for cluster in self.clusters: 
          if cluster.getClusterId() == cluster_id:
               del self.clusters[cluster_index]
               return True
          cluster_index += 1
      return False

  
          
