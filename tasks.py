import json
import pika
from backend.src.admin_requests.api_requests import app_requests
from config import config_instance


def callback(ch, method, properties, body):
    print(" [x] Received %s" % body)
    _body: dict = json.loads(body.decode())
    _func_name: str = _body.get('func')
    _kwargs: dict = _body.get('kwargs')
    if _func_name == app_requests._request.__name__:
        return app_requests._request(**_kwargs)
    elif _func_name == app_requests.get_response.__name__:
        return app_requests.get_response(**_kwargs)
    else:
        pass
    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    while True:
        try:

            connection = pika.BlockingConnection(pika.ConnectionParameters(host=config_instance.RABBIT_MQ_URL))
            channel = connection.channel()
            channel.queue_declare(queue='admin_task_queue', durable=True)

            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(queue='admin_task_queue', on_message_callback=callback)

            channel.start_consuming()
        # Don't recover connections closed by server
        except pika.exceptions.ConnectionClosedByBroker:
            break
        # Don't recover on channel errors
        except pika.exceptions.AMQPChannelError:
            break
        # Recover on all other connection errors
        except pika.exceptions.AMQPConnectionError:
            continue


if __name__ == '__main__':
    print('Admin Starting Task Scheduler')
    try:
        main()
    except Exception as e:
        print(f'Exception Thrown by Admin Task Scheduler : {e}')
