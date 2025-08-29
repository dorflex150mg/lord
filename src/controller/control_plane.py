"""
ControlPlane and main.
"""

from functools import wraps
from typing import Any, Callable, TypeVar
import json
from pika.adapters.blocking_connection import BlockingChannel
from pika import BasicProperties
from controller.service_controller import ServiceController
from entity.service import Service

R = TypeVar("R")  # Return type of the decorated function


class ControlPlane:
    """
    Control Plane
    """

    service_controller: ServiceController = ServiceController()

    @staticmethod
    def cli_endpoint(func: Callable[..., str]) -> Callable[..., str]:
        """
        Decorator for cli endpoints. It responds the caller function with
        the return value of the calling function.
        Args:
            func (Callable[..., Any]): The fuction decorated.
        Returns:
            Callable[..., Any]: The wrapper function.
        """

        @wraps(func)
        def wrapper(
            self,
            channel: BlockingChannel,
            method: Any,
            properties: BasicProperties,
            body: bytes,
        ) -> str:
            output = func(channel, method, properties, body)
            channel.basic_publish(
                exchange="", routing_key=properties.reply_to, body=output.encode()
            )
            channel.basic_ack(delivery_tag=method.delivery_tag)
            return output

        return wrapper  # type: ignore

    @cli_endpoint
    def on_create_service(
        self,
        channel: BlockingChannel,
        method: Any,
        properties: BasicProperties,
        body: bytes,
    ) -> str:
        """
        Callback for the `create_service` endpoint.
        Replies to the caller with service id.
        Args:
            channel (BlockingChannel): the channel.
            method (Any): method used to send,
            properties: (BasicProperties) the properties, including the reply
            routing key.
            body (bytes): empty body.
        """
        reply = json.loads(body.decode())
        return self.service_controller.add_service(
            Service.new(image_name=reply["image_name"])
        )

    @cli_endpoint
    def on_remove_service(
        self,
        channel: BlockingChannel,
        method: Any,
        properties: BasicProperties,
        body: bytes,
    ) -> str:
        """
        Callback for the `on_remove_service` endpoint.
        Replies to the caller with service id.
        Args:
            channel (BlockingChannel): the channel.
            method (Any): method used to send,
            properties: (BasicProperties) the properties, including the reply
            routing key.
            body (bytes): empty body.
        Returns:
            str: String representation of a bool -> `True` if the operation
            has been succesful. False otherwise.
        """
        reply = json.loads(body.decode())
        return str(self.service_controller.remove_service(reply["service_id"]))

    @cli_endpoint
    def on_add_instance_to_service(
        self,
        channel: BlockingChannel,
        method: Any,
        properties: BasicProperties,
        body: bytes,
    ) -> str:
        """
        Callback for the `add_instance_to_service` endpoint.
        Replies to the caller with service id.
        Args:
            channel (BlockingChannel): the channel.
            method (Any): method used to send,
            properties: (BasicProperties) the properties, including the reply
            routing key.
            body (bytes): empty body.
        Returns:
            str: The id of the new service.
        """
        reply = json.loads(body.decode())
        return self.service_controller.add_instance_to_service(reply["service_id"])

    @cli_endpoint
    def on_remove_instance_from_service(
        self,
        channel: BlockingChannel,
        method: Any,
        properties: BasicProperties,
        body: bytes,
    ) -> str:
        """
        Callback for the `add_instance_to_service` endpoint.
        Args:
            channel (BlockingChannel): the channel.
            method (Any): method used to send,
            properties: (BasicProperties) the properties, including the reply
            routing key.
            body (bytes): empty body.
        Returns:
            str: String representation of a bool -> `True` if the operation
            has been succesful. False otherwise.
        """
        reply = json.loads(body.decode())
        return str(
            self.service_controller.remove_instance_from_service(
                instance_id=reply["instance_id"], service_id=reply["service_id"]
            )
        )
