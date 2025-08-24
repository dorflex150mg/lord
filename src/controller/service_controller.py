"""
This Module contains the Service Controller class.
"""
import time
from typing import Dict
from pydantic import BaseModel
from entity.service import Service
from src.docker import docker

BACKOFF = 1 # 1 second.

class ServiceController(BaseModel):
    """
    The ServiceController creates and removes services, as well
    as adding new Instances and removing them from existing 
    Services.
    Attributes:
        services (Dict[str, Service]): Current running Services.
    """
    services: Dict[str, Service] = {}


    def add_service(self, service: Service) -> str:
        """
        Adds a service to the ServiceController.
        Args:
            service (Service): The service to be added.
        """
        docker.build(service.image_name)
        if service.service_id in self.services:
            raise ValueError(f"Service {service.name} already exists.")
        self.services[service.service_id] = service
        return service.service_id

    def remove_service(self, string: str) -> bool:
        """
        Removes a service from the Service Controller.
        Args:
            string (str): id or name of the Service to be removed.
        Returns:
            bool: True if the Service was found.
        Raises:
            IndexError: if there are no services running in this ServiceController.
        """
        if not self.services:
            raise IndexError("There are no services to be removed.")
        if string in self.services:
            self.services.pop(string)
            return True
        matching_service = [service.service_id for service
                            in self.services.values()
                            if service.name == string]
        if matching_service:
            self.services.pop(set(matching_service).pop())
            return True
        return False

    def add_instance_to_service(self, service_id: str) -> str:
        """
        Adds an instance to an existing service.
        Args: 
            service_id (str): The id of the service to gain a new instance.
        Returns:
            str: the id of the new instance created.
        """
        docker.run(self.services[service_id].image_name)
        return self.services[service_id].add_instance()

    def remove_instance_from_service(self, instance_id: str, service_id: str):
        """
        Removes an instance from a service.
        Args:
            instance_id (str): The id of the instance to be removed.
            service_id (str): The id of the service the instance must be removed from.
        Raises:
            IndexError: if there are no services running in this ServiceController.
        """
        if not self.services:
            raise IndexError("There are no services created.")
        self.services[service_id].remove_instance(instance_id)
        while instance_id in docker.ps():
            docker.stop(instance_id)
            time.sleep(BACKOFF)
        docker.rm(instance_id)
