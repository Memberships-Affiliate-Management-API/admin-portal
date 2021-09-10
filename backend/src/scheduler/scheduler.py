"""
    **scheduler**
        used to dynamically add jobs on a separate thread to complete tasks that should not interfere
        with requests, or requests that takes a long time to complete
"""
__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"

import json
import socket
from typing import Callable
import pika

from backend.src.custom_exceptions.exceptions import status_codes

connection = None


def create_task(func: Callable, kwargs: dict, delay: int = 10, job_name: str = "create_task") -> tuple:
    """

    """
    global connection
    # noinspection PyUnresolvedReferences
    _body: bytes = json.dumps(dict(func=func.__name__, kwargs=kwargs, job_name=job_name)).encode(encoding='UTF-8')

    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='amqps:memberships-rabbitmq'))
        channel = connection.channel()
        channel.queue_declare(queue='admin_task_queue', durable=True)
        channel.basic_publish(
            exchange='',
            routing_key='task_queue',
            body=_body,
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            ))

    except pika.exceptions.ConnectionClosedByBroker as e:
        print(f'Create Task Error: {e}')
        pass
    # Don't recover on channel errors
    except pika.exceptions.AMQPChannelError as e:
        print(f'Create Task Error: {e}')
        pass
    # Recover on all other connection errors
    except pika.exceptions.AMQPConnectionError as e:
        print(f'Create Task Error: {e}')
        pass
    except socket.gaierror as e:
        print(f'Create Task Error: {e}')
        pass
    finally:
        if not not connection:
            connection.close()

    return _body, status_codes.status_ok_code
