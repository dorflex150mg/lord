"""
ControlPlane and main.
"""

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
        self, channel: BlockingChannel, method, properties: BasicProperties, body
    ):
        service_id = self.service_controller.add_service(Service.new())
        channel.basic_publish(exchange="", routing_key=properties.reply_to)
