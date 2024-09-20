from random import choice, randint
import pika
from faker import Faker

from models import Task


credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

exchange = "Some service"

channel.exchange_declare(exchange, exchange_type="direct")
channel.queue_declare("sms_publish", durable=True)
channel.queue_declare("email_publish", durable=True)
channel.queue_bind(exchange=exchange, queue="sms_publish")
channel.queue_bind(exchange=exchange, queue="email_publish")

faker = Faker("uk-UA")
methods = ["sms_publish", "email_publish"]

def create_task(n:int):
    for i in range(n):
        task = Task(name=faker.name(),
                    age=randint(10, 75),
                    email=faker.email(),
                    phone=faker.phone_number(),
                    preferred_method=choice(methods))
        task.save()
        channel.basic_publish(
            exchange=exchange,
            routing_key=task.preferred_method,
            body=str(task.id).encode(),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ))
    connection.close()
     
if __name__=="__main__":
    create_task(10)   
        