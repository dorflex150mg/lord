"""
Cluster Module
"""
from typing import Dict 

from node import Node
from load_balancer import LoadBalancer
from instance import Instance
from pydantic import BaseModel, Field

from util import consts

class Cluster(BaseModel):
    """
    Cluster Base Model class. It represents an application cluster that spams across
    multiple nodes. These nodes will have instances of the application. It also 
    contains the Load Balancers that control traffic to the application. It has an 
    id and a name.

    """

    cluster_id: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    instances: Dict[str, Instance] = {}
    nodes: Dict[str, Node] = {}
    nodes: Dict[str, Node] = {}
    load_balancers: Dict[str, LoadBalancer] = {}

    def add_instance(self, instance: Instance) -> None:
        if len(self.instances) >= consts.MAX_INSTANCES:
            raise ValueError(f"Cluster {self.name} has the maximum instance "
                             f"count and cannot add instance {instance.name} ")
        if instance.node_id in self.nodes:
            self.nodes[instance.node_id].add_instance(instance)
        self.instances[instance.id] = instance

    def remove_instance(self, instance_id: str) -> bool:
        if not self.instances:
            raise IndexError(f"There are no instances to remove from node {self.name}")
        if self.instances.pop(instance_id):
            for node in self.nodes.values():
                if instance_id in node.instances:
                    node.remove_instance(instance_id)
            return True
        return False


    def add_node(self, node: Node) -> None:
        if len(self.nodes) >= consts.MAX_NODES:
            raise ValueError(f"Cluster {self.name} has the maximum node "
                             f"count and cannot add node {node.name} ")
        self.nodes[node.id] = node

    def remove_node(self, node_id: str) -> bool:
        if not self.nodes:
            raise IndexError(f"There are no nodes to remove from node {self.name}")
        if self.nodes.pop(node_id):
            return True
        return False

    def add_load_balancer(self, load_balancer: LoadBalancer) -> None:
        if len(self.load_balancers) >= consts.MAX_LOAD_BALANCERS:
            raise ValueError(f"Cluster {self.name} has the maximum load_balancer "
                             f"count and cannot add load_balancer {load_balancer.name} ")
        self.load_balancers[load_balancer.get_load_balancer_id()] = load_balancer


    def remove_load_balancer(self, load_balancer_id: str) -> bool:
        if not self.load_balancers:
            raise IndexError("There are no load balancers to remove from {self.name}")
        if self.load_balancers.pop(load_balancer_id):
            return True
        return False
