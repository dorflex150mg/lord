# pylint: disable=missing-function-docstring, missing-class-docstring, missing-module-docstring
import unittest
from src.controller.service_controller import ServiceController
from src.docker.docker import subprocess
from src.entity.service import Service


class ServiceControllerTest(unittest.TestCase):

    def setUp(self) -> None:
        subprocess.call(
            ["docker", "rmi", "-f", "ubuntu-example"]
        )  # Removes test image.
        return super().setUp()

    def test_create_service(self) -> None:
        service_controller = ServiceController()
        service = Service.new(image_name="ubuntu-example", name="test_create_service")
        image_id = service_controller.add_service(service)
        image_ids = subprocess.check_output(["docker", "images", "-q"]).split()
        image_ids = [image_id.decode() for image_id in image_ids]
        assert image_id in image_ids
        assert service.service_id in service_controller.list_services()

    def test_remove_service(self) -> None:
        service_controller = ServiceController()
        service = Service.new(image_name="ubuntu-example", name="test_remove_service")
        image_id = service_controller.add_service(service)
        image_ids = subprocess.check_output(["docker", "images", "-q"]).split()
        image_ids = [image_id.decode() for image_id in image_ids]
        assert image_id in image_ids
        service_controller.remove_service(service.service_id)
        image_ids = subprocess.check_output(["docker", "images", "-q"]).split()
        image_ids = [image_id.decode() for image_id in image_ids]
        assert image_id in image_ids  # The image does not get removed.
        assert service.service_id not in service_controller.list_services()

    def test_add_instance_to_service(self) -> None:
        subprocess.call(
            ["docker", "ps", "-q", "|", "xargs", "docker", "rm", "-f"]
        )  # Removes all containers.
        service_controller = ServiceController()
        service = Service.new(
            image_name="ubuntu-example", name="test_add_instance_service"
        )
        service_controller.add_service(service)
        instance_id = service_controller.add_instance_to_service(service.service_id)
        container_ids = [
            container_id.decode()
            for container_id in subprocess.check_output(["docker", "ps", "-q"]).split()
        ]
        assert instance_id in container_ids
        service_controller.remove_instance_from_service(instance_id, service.service_id)
        container_ids = [
            container_id.decode()
            for container_id in subprocess.check_output(["docker", "ps", "-q"]).split()
        ]
        assert instance_id not in container_ids
        assert instance_id not in service.instances

    def test_list_services(self) -> None:
        service_controller = ServiceController()
        service = Service.new(
            image_name="ubuntu-example", name="test_list_service"
        )
        service_controller.add_service(service)
        assert service.service_id in service_controller.list_services()
        service_controller.remove_service(service.service_id)
        assert service.service_id not in service_controller.list_services()

if __name__ == "__main__":
    unittest.main()
