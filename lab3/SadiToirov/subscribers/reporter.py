import json
from datetime import datetime

from pika import BlockingConnection, ConnectionParameters, PlainCredentials

RMQ_HOST = 'localhost'
RMQ_USER = 'rabbit'
RMQ_PASS = '1234'
EXCHANGE_NAME = 'amq.topic'
ROUTING_KEY = 'rep.*'
LOG_FILE = 'receiver.log'

def get_latest_value():
    with open(LOG_FILE, 'r') as f:
        lines = f.readlines()
        if not lines:
            return None
        return int(json.loads(lines[-1])['co2'])


def calculate_average_value():
    with open(LOG_FILE, 'r') as f:
        lines = f.readlines()
        if not lines:
            return None
        
        co2_values = [int(json.loads(line)['co2']) for line in lines]
        return sum(co2_values) / len(co2_values)


def callback(channel, method, properties, body):
    data = json.loads(body)
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if data['query'] == 'current':
        latest_value = get_latest_value()
        if latest_value is not None:
            message = f"{current_time}: Latest CO2 level is {latest_value}"
        else:
            message = f"{current_time}: No data available for `current`"
            
    elif data['query'] == 'average':
        avg_value = calculate_average_value()
        if avg_value is not None:
            message = f"{current_time}: Average CO2 level is {avg_value}"
        else:
            message = f"{current_time}: No data available for `average`"
    else:
        message = f"{current_time}: Invalid query '{data['query']}'"

    print(message)


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
    
    channel.basic_consume(
        queue=queue_name,
        on_message_callback=callback,
        auto_ack=True
    )
    
    print('[*] Waiting for queries from the control tower. Press CTRL+C to exit')
    channel.start_consuming()
    
    connection.close()
