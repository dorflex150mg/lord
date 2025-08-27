"""
Network related utilities.
"""

import socket
from enum import Enum


class IpType(Enum):
    """
    Enum that defines the socket family type
    """

    V4 = 0
    V6 = 1


def get_local_ip(ip_type: IpType) -> str:
    """
    Creates a connection to an external bogus ip and reads the socket's ip.
    Returns:
        str: The socket's ip used to get to an external network.
    """
    family = None
    external_ip = None
    if ip_type == IpType.V6:
        family = socket.AF_INET6
        external_ip = "3f1a:9c4d:72b0:1e5f:8d23:4a9c:bd71:92ef"
    else:
        family = socket.AF_INET
        external_ip = "10.254.254.254"
    s = socket.socket(family, socket.SOCK_DGRAM)
    s.settimeout(0)
    s.connect_ex((external_ip, 1))
    ip = s.getsockname()[0]
    ip = "127.0.0.1" if ip == "0.0.0.0" else ip
    s.close()
    return ip


def get_local_ipv4() -> str:
    """
    Returns the local node's ipv4.
    """
    return get_local_ip(IpType.V4)


def get_local_ipv6() -> str:
    """
    Returns the local node's ipv6.
    """
    return get_local_ip(IpType.V6)
