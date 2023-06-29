import pika
from models import Contact
import time
import json
import mongoengine
import pickle
from connect import Atlas_Server

server = Atlas_Server("config-client-db.ini")
server.connect()

"""
connect to Rabbit (installed on Docker on the port 5672)
"""
credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))

channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')

"""
work with the db when recieve a message
"""


def callback(ch, method, properties, body):
    message = pickle.loads(body)
    print(f" [x] Received {message}")
    time.sleep(1)

    contact_id = message["id"]
    contact = Contact.objects(id=contact_id)
    contact.update(sent=True)

    print(f" [x] Email sent: {method.delivery_tag}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=callback)


if __name__ == '__main__':
    channel.start_consuming()
