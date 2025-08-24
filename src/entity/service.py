"""
Service Module
"""

from typing import Dict

import uuid


from node import Node
from load_balancer import LoadBalancer
from instance import Instance
from pydantic import BaseModel, Field
from scheduler import scheduler
from util.name_generator import NameGenerator

from util import consts


class Service(BaseModel):
    """
    Service Base Model class. It represents an application service that spams across
    multiple nodes. These nodes will have instances of the application. It also
    contains the Load Balancers that control traffic to the application. It has an
    id and a name.
    Attributes:
        service_id (str): The unique id of the service.
        name (str): the human-readable name of the service.
        instances (Dict[str, Instance]): the application instances in this service.
        nodes: (Dict[str, Node]) the nodes accessible by this service.
        load_balancers (Dict[str, LoadBalancer]): the load_balancers setup on the service.
    """

    service_id: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    image_name: str = Field(..., min_length=1)
    instances: Dict[str, Instance] = {}
    nodes: Dict[str, Node] = {}
    load_balancers: Dict[str, LoadBalancer] = {}

    @classmethod
    def new(cls, image_name) -> "Service":
        """
        Creates a new service with random name and id.
        Returns:
            Service: the new Service.
        """
        return Service(service_id=str(uuid.uuid4()), image_name=image_name, name=NameGenerator.generate_name())

    def add_instance(self) -> str:
        """
        Adds an instance to this Service. The instance's node
        id is used to determine to which node it should go.
        Args:
            instance: The instance to be added to this service.
        Raises:
            ValueError: if the number of instances is past the maximum.
            ValueError: if the instance does not have a valid node id.
        """
        if len(self.instances) >= consts.MAX_INSTANCES:
            raise ValueError(
                f"Service {self.name} has the maximum instance "
                f"count and cannot add another instance."
            )
        new_instance = Instance(
            instance_id=str(uuid.uuid4()),
            name=NameGenerator.generate_name(),
            node_id=scheduler.get_next(list(self.nodes.values())),
        )
        self.nodes[new_instance.node_id].add_instance(new_instance)
        self.instances[new_instance.instance_id] = new_instance
        return new_instance.instance_id

    def remove_instance(self, instance_id: str) -> bool:
        """
        Removes an instance from the service and from the node it has
        been scheduled to.
        Args:
            instance_id (str): the id of the instance to remove.
        Raises:
            IndexError: if there are no instances to remove.
        Return:
            bool: True if the instance existed in this service.
        """
        if not self.instances:
            raise IndexError(
                f"There are no instances to remove from Service {self.name}"
            )
        if self.instances.pop(instance_id):
            for node in self.nodes.values():
                if instance_id in node.instances:
                    node.remove_instance(instance_id)
            return True
        return False

    def add_node(self, node: Node) -> None:
        """
        Adds a new node to this service.
        Args:
            node (Node): The node to be added.
        Raises:
            ValueError: if the number of instances is past the maximum.
            ValueError: if the node already exists in this Service.
        """
        if len(self.nodes) >= consts.MAX_NODES:
            raise ValueError(
                f"Service {self.name} has the maximum node "
                f"count and cannot add node {node.name} "
            )
        if node in self.nodes:
            raise ValueError(
                f"Node {node.name} is already scheduled to Service {self.name}"
            )
        self.nodes[node.id] = node

    def remove_node(self, node_id: str) -> bool:
        """
        Removes a node from this service.
        Args:
            node_id (str): The id of the node to be removed.
        Returns:
            bool: True if the node existed in this Service.
        Raises:
            IndexError: if there are no modes in this Service.
        """
        if not self.nodes:
            raise IndexError(f"There are no nodes to remove from node {self.name}")
        if self.nodes.pop(node_id):
            return True
        return False

    def add_load_balancer(self, load_balancer: LoadBalancer) -> None:
        """
        Adds a load balancer to this Service.
        Args:
            load_balancer (LoadBalancer): the load balancer to add.
        Raises:
            ValueError: If the number of load_balancers is past the maximum.
        """
        if len(self.load_balancers) >= consts.MAX_LOAD_BALANCERS:
            raise ValueError(
                f"Service {self.name} has the maximum load_balancer "
                f"count and cannot add load_balancer {load_balancer.name} "
            )
        self.load_balancers[load_balancer.id] = load_balancer

    def remove_load_balancer(self, load_balancer_id: str) -> bool:
        """
        Removes a load balancer from this Service.
        Args:
            load_balancer_id (str): The id of the load balancer to be removed.
        Returns:
            True if the load balancer existed in this Service.
        Raises:
            IndexError: If there are no more load balancers in this Service.
        """
        if not self.load_balancers:
            raise IndexError("There are no load balancers to remove from {self.name}")
        if self.load_balancers.pop(load_balancer_id):
            return True
        return False
