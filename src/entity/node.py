from typing import Dict

from pydantic import BaseModel, Field
from instance import Instance
from network.node_network import NodeNetwork

from utils import consts


class Node(BaseModel):
    id: str = Field(..., min_length=1) 
    name: str =  Field(..., min_length=1) 
    node_network: NodeNetwork
    instances: Dict[str, Instance] = {}

    def add_instance(self, instance: Instance) -> None:
        if len(self.instances) >= consts.MAX_INSTANCES:
            raise ValueError(f"Node {self.name} has the maximum instance "
                             f"count and cannot add instance {instance.name} ")
        self.instances[instance.id] = instance

    def remove_instance(self, instance_id: str) -> bool:
        if not self.instances:
            raise IndexError(f"There are no instances to remove from node {self.name}")
        if self.instances.pop(instance_id):
            return True
        return False
