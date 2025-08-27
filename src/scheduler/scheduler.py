"""
This module provides methods to assist on the scheduling
of a service's nodes.
"""

from typing import List
from src.entity.node import Node


def get_next(nodes: List[Node]) -> str:
    """
    Returns the node with fewer instances.
    Args:
        nodes: The service's nodes.
    """
    nodes.sort(key=lambda node: len(node.instances))
    if not nodes:
        raise ValueError("No nodes available.")
    return nodes[0].node_id
