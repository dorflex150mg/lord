"""
ControlPlane and main.
"""

from typing import Any
import json
import pika
from pika.adapters.blocking_connection import BlockingChannel
from pika import BasicProperties
from controller.service_controller import ServiceController
from entity.service import Service


class ControlPlane:
    """
    Control Plane
    """

    service_controller: ServiceController = ServiceController()

    def on_create_service(
        self, channel: BlockingChannel, method: Any, properties: BasicProperties, body
    ):
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
        service_id = self.service_controller.add_service(
            Service.new(image_name=reply["image_name"])
        )
        channel.basic_publish(
            exchange="", routing_key=properties.reply_to, body=service_id.encode()
        )
        channel.basic_ack(delivery_tag=method.delivery_tag)
