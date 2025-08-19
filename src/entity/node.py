"""
Module containing the Node Base Model
"""

from typing import Dict

from pydantic import BaseModel, Field
from instance import Instance
from network.node_network import NodeNetwork

from util import consts


class Node(BaseModel):
    """
    This class represents a physical node. Nodes contain the instances
    of the applications running in it.
    Attributes:
        id (str): the unique id.
        name (str): the human-readable name.
        node_network (NodeNetwork): a dataclass containing the network information 
        for that node.
        instances (Dict[str, Instance]): The application instances scheduled 
        to this node.
    """
    id: str = Field(..., min_length=1)
    name: str =  Field(..., min_length=1)
    node_network: NodeNetwork
    instances: Dict[str, Instance] = {}

    def add_instance(self, instance: Instance) -> None:
        """
        Adds an application instance to this node.
        Args:
            instance (Instance): The instance to be added.
        """
        if len(self.instances) >= consts.MAX_INSTANCES:
            raise ValueError(f"Node {self.name} has the maximum instance "
                             f"count and cannot add instance {instance.name} ")
        self.instances[instance.id] = instance

    def remove_instance(self, instance_id: str) -> bool:
        """
        Removes an application instance from this node.
        Args:
            instance_id (str): the id of the instance to be removed.
        Returns:
            bool: True if the instance existed in this Node.
        Raises:
            IndexError: if there were no instances in this node.
        """
        if not self.instances:
            raise IndexError(f"There are no instances to remove from node {self.name}")
        if self.instances.pop(instance_id):
            return True
        return False
