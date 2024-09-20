import pika

from models import Task

def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()
    
    exchange = "Some service"

    channel.exchange_declare(exchange, exchange_type="direct")
    channel.queue_declare("sms_publish", durable=True)
    channel.queue_declare("email_publish", durable=True)
    channel.queue_bind(exchange=exchange, queue="sms_publish")
    channel.queue_bind(exchange=exchange, queue="email_publish")
    print(' [*] Waiting for messages. To exit press CTRL+C')
    
    def callback(ch, method, properties, body):
        message = body.decode()
        print(f" [x] Received {message}")
        task = Task.objects(id=message, completed=False).first()
        if task:
            task.update(set__completed=True)
        print(f" [x] Done: {method.delivery_tag}")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue="sms_publish", on_message_callback=callback)
    channel.basic_consume(queue="email_publish", on_message_callback=callback)
    
    channel.start_consuming()
    
if __name__=="__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")