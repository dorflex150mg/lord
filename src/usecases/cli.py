"""
CLI for Lord. Communicates with the control plane via RabbitMQ
"""

from typing import Dict, Optional
import argparse
import pika
import uuid
from pika import BasicProperties
import msgpack
from pika.adapters.blocking_connection import BlockingChannel


class Connection:
    """
    Wrapper class around the RabbitMQ connection.
    """

    connection: pika.BlockingConnection = pika.BlockingConnection(
        pika.ConnectionParameters("localhost")
    )
    response_slot: Optional[bytes] = None

    @classmethod
    def get_connection(cls):
        """
        Getter for the connection.
        """
        return cls.connection


def get_service_id(channel, method, properties, body) -> None:
    Connection.response_slot = body
    print(body.decode())


def listen_to_service_id(channel: BlockingChannel, callback_queue):
    channel.basic_consume(
        queue=callback_queue, on_message_callback=get_service_id, auto_ack=True
    )


def create_service(args):
    """
    Sends a request to create a new service
    to the ControlPlane
    """
    channel = Connection.connection.channel()
    oneshot_id = str(uuid.uuid4())

    result = channel.queue_declare(queue="", exclusive=True)
    callback_queue = result.method.queue

    listen_to_service_id(channel, callback_queue)  # waits for the service id

    channel.queue_declare(queue="create_service")
    service_data: Dict[str, str] = {"name": args.name}
    channel.basic_publish(
        exchange="",
        routing_key="create_service",
        properties=BasicProperties(reply_to=callback_queue, correlation_id=oneshot_id),
        body=msgpack.dumps(service_data),  # pyright: ignore[reportArgumentType]
    )
    while not Connection.response_slot:
        Connection.connection.process_data_events()
    Connection.response_slot = None


def main():
    """
    CLI's main. Parses through input and
    makes request via rabbitmq to the
    control plane.
    """
    parser = argparse.ArgumentParser(
        prog="Lord Control Plane CLI",
        description="This CLI provides access to Lord's Control Plane functionality.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    create_parser = subparsers.add_parser("create", help="Create a Lord Resource")
    create_subparsers = create_parser.add_subparsers(required=True)
    service_parser = create_subparsers.add_parser("service", help="Creates a service.")
    service_name_subparser = service_parser.add_subparsers()
    service_name_parser = service_name_subparser.add_parser(
        "--name", help="Sets the name."
    )
    service_name_parser.add_argument("service_name", type=str)
    service_name_parser.set_defaults(func=create_service)


if __name__ == "__main__":
    main()
