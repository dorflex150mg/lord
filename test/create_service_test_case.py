# pylint: disable=missing-function-docstring, missing-class-docstring, missing-module-docstring
import uuid
import unittest
from src.controller.service_controller import ServiceController
from src.docker.docker import subprocess
from src.entity.service import Service


class ServiceControllerTest(unittest.TestCase):

    def test_create_service(self) -> None:
        subprocess.call(["docker", "rmi", "-f", "UbuntuExample"])  # Removes test image.
        service_controller = ServiceController()
        service = Service(
            service_id=str(uuid.uuid4),
            name="test_create_service",
            image_name="UbuntuExample",
        )
        service_id = service_controller.add_service(service)
        image_ids = subprocess.check_output(["docker", "images", "-q"]).split()
        assert service_id in image_ids
        assert service_id in service_controller.list_services()

    def test_remove_service(self) -> None:
        subprocess.call(["docker", "rmi", "-f", "UbuntuExample"])  # Removes test image.
        service_controller = ServiceController()
        service = Service(
            service_id=str(uuid.uuid4),
            name="test_remove_service",
            image_name="UbuntuExample",
        )
        service_id = service_controller.add_service(service)
        image_ids = subprocess.check_output(["docker", "images", "-q"]).split()
        assert service_id in image_ids
        service_controller.remove_service(service_id)
        image_ids = subprocess.check_output(["docker", "images", "-q"]).split()
        assert service_id in image_ids  # The image does not get removed.
        assert service_id not in service_controller.list_services()

    def test_add_instance_to_service(self) -> None:
        subprocess.call(["docker", "rmi", "-f", "UbuntuExample"])  # Removes test image.
        subprocess.call(
            ["docker", "ps", "-q", "|", "xargs", "docker", "rm", "-f"]
        )  # Removes all containers.
        service_controller = ServiceController()
        service = Service(
            service_id=str(uuid.uuid4),
            name="test_add_instance_service",
            image_name="UbuntuExample",
        )
        service_id = service_controller.add_service(service)
        instance_id = service_controller.add_instance_to_service(service_id)
        container_ids = subprocess.check_output(["docker", "ps", "-q"]).split()
        assert instance_id in container_ids


if __name__ == "__main__":
    unittest.main()
