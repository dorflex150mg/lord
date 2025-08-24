"""
Module containing docker bindings. This high-level module
Simply makes subprocess calls to the docker CLI.
"""

from typing import Dict, List
import subprocess
import os

DOCKERFILE_SOURCES = os.getcwd()

ps_values: Dict[str, int] = {
    "CONTAINER_ID": 0,
    "IMAGE": 1,
    "COMMAND": 2,
    "CREATED": 3,
    "STATUS": 4,
    "PORTS": 5,
    "NAMES": 6,
}
INSPECT_GET_IP_QUERY = "{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}"
DEFAULT_VOLUME_PATH = "/src/volume"
NETWORKID_STRING_START_POSITION = 14
NETWORKID_STRING_END_POSITION = -2
IPADDRESS_STRING_START_POSITION = 14
IPADDRESS_STRING_END_POSITION = -2


def build(tag_name: str, *opts: str) -> int:
    """
    Builds an image with the given parameters (quiet mode by default)
    Args:
        opts (args): list of arguments to be added to the build call.
    Returns:
        int: The process' exit signal.
    """
    args = ["docker", "build", "-t", tag_name] + list(opts)
    args.append(".")
    path = f"{DOCKERFILE_SOURCES}/{tag_name}"
    if not os.path.isdir(path):
        os.mkdir(path)
    return subprocess.call(args, cwd=path)


def rmi(image_id: str, *opts: str) -> int:
    """
    Removes an image with the given parameters.
    Forcefully removes containers running with that image.
    Args:
        image_id (str): the id of the image to be removed.
        opts (args): list of arguments to be added to the rmi call.
    Returns:
        int: The process' exit signal.
    """
    args = ["docker", "rmi"] + list(opts)
    args.append(image_id)
    return subprocess.call(args)


def run(image_id: str, *opts: str) -> int:
    """
    Creates an instance with the given parameters
    Args:
        opts (args): list of arguments to be added to the run call.
    Returns:
        int: The process' exit signal.
    """
    args = ["docker", "run", "-d"] + list(opts)
    args.append(image_id)
    return subprocess.call(args)


def run_get_name(*opts: str) -> str:
    """
    Creates an instance with the given parameters and returns its name.
    Args:
        opts (args): list of arguments to be added to the run call.
    Returns:
        str: The newly created docker container name.
    """
    args = ["docker", "run"] + list(opts)
    return subprocess.check_output(args, stderr=subprocess.STDOUT).decode()


def rm(container_id: str, *opts: str) -> int:
    """
    Removes an container.
    Args:
        container_id (str): the id of the container to be removed.
        opts (args): list of arguments to be added to the rm call.
    Returns:
        int: The process' exit signal.
    """
    args = ["docker", "rm", container_id] + list(opts)
    return subprocess.call(args)


def stop(container_id: str, *opts: str) -> int:
    """
    Stops a running container.
    Args:
        opts (args): list of arguments to be added to the stop call.
    Returns:
        int: The process' exit signal.
    """
    args = ["docker", "stop", container_id] + list(opts)
    return subprocess.call(args)


def ps(*opts: str) -> List[str]:
    """
    Lists the containers running currently. Removes the first and last elements.
    Args:
        opts (args): list of arguments to be added to the ps call.
    Returns:
        List[str]: A list with the docker id of the containers running
        in this node.
    """
    args = ["docker", "ps", "-q"] + list(opts)
    return (
        subprocess.check_output(args, stderr=subprocess.STDOUT).decode().split(sep="\n")
    )


def images(*opts: str) -> int:
    """
    Lists the docker images stored on this node.
    Args:
        opts (args): list of arguments to be added to the images call.
    Returns:
        List[str]: A list with the docker id of the images stored
        in this node.
    """
    args = ["docker", "images"] + list(opts) + list(opts)
    return subprocess.call(args)


def inspect(resource_id: str, *opts: str) -> str:
    """
    Returns metadata from a docker resource.
    Args:
        opts (args): list of arguments to be added to the inspect call.
    Returns:
        str: a string with the the output of the inspect call.
    """
    args = ["docker", "inspect", resource_id] + list(opts)
    return subprocess.check_output(args, stderr=subprocess.STDOUT).decode()


def create_volume(host_path: str, container_path: str, *opts: str) -> int:
    """
    Creates a volume binding `host_path` and `container_path`.
    Args:
        host_path (str): the path on the host.
        container_path (str): the target path on the container.
    Returns:
        int: The process' exit signal.
    """
    args = [
        "docker",
        "volume",
        "create",
        "-d",
        "-v",
        f"{host_path}:{container_path}",
    ] + list(opts)
    return subprocess.call(args)


def remove_volume(volume_id: str, *opts: str) -> int:
    """
    Removes a volume.
    Args:
        opts (args): list of arguments to be added to the remove_volume call.
    Returns:
        int: The process' exit signal.
    """
    args = ["docker", "volume", "rm", volume_id] + list(opts)
    return subprocess.call(args)


def cp(*opts: str) -> int:
    """
    Copies files from instances to containers and vice versa
    Args:
        opts (args): list of arguments to be added to the cp call.
    Returns:
        int: The process' exit signal.
    """
    args = ["docker", "cp"] + list(opts)
    return subprocess.call(args)


def create_network(*opts: str) -> int:
    """
    Creates a network with the given parameters
    Args:
        opts (args): list of arguments to be added to the create_network call.
    Returns:
        int: The process' exit signal.
    """
    args = ["docker", "network", "create", "--driver", "bridge"] + list(opts)
    return subprocess.call(args)


def remove_network(*opts: str) -> int:
    """
    Removes a network with the given parameter.
    Args:
        opts (args): list of arguments to be added to the remove_network call.
    Returns:
        int: The process' exit signal.
    """
    args = ["docker", "network", "rm"] + list(opts)
    return subprocess.call(args)


def get_instance_names_by_id(image_id: str) -> List[str]:
    """
    Returns the nameIsso quer dizer que eu estou dentro do prazo estipulado? of the containers running an image by image id.
    Args:
        image_id (str): the id of the image.
    Returns:
        List[str]: a list of the ids of the  containers with that image.
    """
    return ps("--filter", "ancestor=" + image_id)


def _is_ip_line(line: str) -> bool:
    return line.strip().startswith('"IPAddress')


def get_ips_by_id(image_id: str) -> list[str]:
    """
    retuns the ips from containers running an image by image id.
    Args:
        image_id(str): the image id of the containers whose ips
        we return.
    Returns:
        list(str): a list of the ips.
    """
    container_names = get_instance_names_by_id(image_id)
    ip_lines = [
        list(filter(_is_ip_line, inspect(container_id).split("\n"))).pop()
        for container_id in container_names
    ]
    return [ip_line.split()[-1].strip('"') for ip_line in ip_lines]
