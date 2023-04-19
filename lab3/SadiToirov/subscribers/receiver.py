import json
from datetime import datetime

from pika import BlockingConnection, ConnectionParameters, PlainCredentials

RMQ_HOST = 'localhost'
RMQ_USER = 'rabbit'
RMQ_PASS = '1234'
EXCHANGE_NAME = 'amq.topic'
ROUTING_KEY = 'co2.*'


def callback(channel, method, properties, body):
    
    data = json.loads(body)
    time_str = data['time']
    co2_value = int(data['co2'])
    datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
    
    with open('receiver.log', 'a') as f:
        f.write(json.dumps(data) + "\n")
    
    if co2_value > 500:
        print(f"{time_str}: WARNING")
    else:
        print(f"{time_str}: OK")


if __name__ == '__main__':
    credentials = PlainCredentials(RMQ_USER, RMQ_PASS)
    parameters = ConnectionParameters(host=RMQ_HOST, credentials=credentials)
    connection = BlockingConnection(parameters)
    channel = connection.channel()
    
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(
        exchange=EXCHANGE_NAME,
        queue=queue_name,
        routing_key=ROUTING_KEY
    )
    
    print("[*] Waiting for CO2 data. Press CTRL+C to exit")
    channel.basic_consume(
        queue=queue_name,
        on_message_callback=callback,
        auto_ack=True
    )
    channel.start_consuming()
