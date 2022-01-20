import pika
import json
from send import Email

# conectando ao rabbitMQ
credentials = pika.PlainCredentials('****tic', 'Atl*******')
parameters = pika.ConnectionParameters(host='**.***.***.**', port='****', credentials=credentials, heartbeat=0)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

def callback(channel, method, properties, boby):
    # lendo a fila é enviando por email
    Email(json.loads(boby), boby)

def start():
    # consumindo fila
    channel.basic_consume(queue='QueuePaymentChargeback', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

start()