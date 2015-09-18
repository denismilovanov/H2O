import json
import pika

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QueueBag:
    def __init__(self, channel, method, queue):
        self.channel = channel
        self.method = method
        self.queue = queue

class GeneralTask:
    def __init__(self, task_data, bag):
        self.bag = bag
        self.task_data = task_data

    def __str__(self):
        return str(self.task_data)

    def commit(self):
        self.bag.channel.basic_ack(delivery_tag=self.bag.method.delivery_tag)

    def rollback(self, delay, max_attempts=10):
        # inc attempts count
        self.task_data['attempts'] += 1
        # check
        if self.task_data['attempts'] > max_attempts:
            # remove old by ack
            self.commit()
            return

        channel = self.bag.channel
        hold_queue = self.bag.queue + '_delayed_' + str(delay)

        hold_queue_arguments = {
            "x-dead-letter-exchange": self.bag.queue,
            "x-dead-letter-routing-key": self.bag.queue,
            "x-message-ttl": delay * 1000,
        }
        self.bag.channel.exchange_declare(exchange=hold_queue, durable=True)
        self.bag.channel.queue_declare(queue=hold_queue, durable=True, exclusive=False, arguments=hold_queue_arguments)
        self.bag.channel.queue_bind(exchange=hold_queue, queue=hold_queue, routing_key=hold_queue)

        # remove old by ack
        self.commit()
        # publish new
        self.bag.channel.basic_publish(
            exchange='',
            routing_key=hold_queue,
            body=json.dumps(self.task_data),
            properties=pika.BasicProperties(delivery_mode=2,),
        )

class MockTask:
    def __init__(self, task_data):
        self.bag = None
        self.task_data = task_data

    def commit(self):
        logger.info('mock commit')

    def rollback(self, delay, max_attempts=10):
        logger.info('mock rollback')

class Queue:
    test = True
    test_prefix = '__test_'

    @staticmethod
    def get_queue_name(queue):
        if Queue.test and not queue.startswith(Queue.test_prefix):
            return Queue.test_prefix + queue
        return queue

    @staticmethod
    def get_channel():
        from H2O.settings import RABBITMQ_USER, RABBITMQ_PASSWORD, RABBITMQ_HOST, RABBITMQ_PORT
        credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
        connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST, RABBITMQ_PORT, '/', credentials))
        channel = connection.channel()
        return channel, connection

    @staticmethod
    def push(queue, message):
        queue = Queue.get_queue_name(queue)
        logger.info('Enqueue into ' + str(queue) + ' ' + str(message))
        channel, connection = Queue.get_channel()
        channel.queue_declare(queue=queue, durable=True)
        channel.exchange_declare(exchange=queue, durable=True)
        channel.queue_bind(exchange=queue, queue=queue, routing_key=queue)
        message['attempts'] = 1
        body = json.dumps(message)
        channel.basic_publish(exchange=queue, routing_key=queue, body=body)
        connection.close()

    @staticmethod
    def subscribe(queue, call):
        queue = Queue.get_queue_name(queue)

        def callback(channel, method, properties, body):
            task = json.loads(body)
            call(GeneralTask(task, QueueBag(channel, method, queue)))

        channel, _ = Queue.get_channel()
        channel.queue_declare(queue=queue, durable=True)
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(callback, queue=queue, no_ack=False)
        channel.start_consuming()

