import pika
from src.controller.control_plane import ControlPlane


def main():
    control_plane = ControlPlane()
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    channel.queue_delete(queue="create_service")
    channel.basic_qos(prefetch_size=1)
    channel.basic_consume(
        queue="create_service", on_message_callback=control_plane.on_create_service
    )
    channel.start_consuming()
