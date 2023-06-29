import faker
from models import Contact
from connect import Atlas_Server
import mongoengine
from random import randrange
import pika
import json
import pickle

MIN_CLIENT = 20
MAX_CLIENT = 40

server = Atlas_Server("config-client-db.ini")
server.connect()
"""
define randomly number of contacts
"""
num_clients = randrange(MIN_CLIENT, MAX_CLIENT)
# print(num_clients)

"""
define randomly names and emails and create a contact and put it into db
"""

for i in range(num_clients):
    fake = faker.Faker()
    email1 = fake.email()
    fullname1 = fake.name()
    contact = Contact(fullname=fullname1, email=email1)
    contact.save()


"""
create connection with the Rabbit (was installed on Docker port 5672)
"""

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))

channel = connection.channel()
channel.exchange_declare(exchange='task_mock', exchange_type='direct')
channel.queue_declare(queue='task_queue', durable=True)
channel.queue_bind(exchange='task_mock', queue='task_queue')

"""
generate for each contact from db message, encode it and send to Rabbit
"""

for contact in Contact.objects:
    message = {
        "id": contact.id
    }

    channel.basic_publish(
        exchange='task_mock',
        routing_key='task_queue',
        body=pickle.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
        ))
    print(" [x] Sent %r" % message)

connection.close()
