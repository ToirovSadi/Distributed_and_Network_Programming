import json
from datetime import datetime

from pika import BlockingConnection, ConnectionParameters, PlainCredentials

RMQ_HOST = 'localhost'
RMQ_USER = 'rabbit'
RMQ_PASS = '1234'
EXCHANGE_NAME = 'amq.topic'
ROUTING_KEY = 'co2.sensor'

if __name__ == '__main__':
    credentials = PlainCredentials(RMQ_USER, RMQ_PASS)
    parameters = ConnectionParameters(host=RMQ_HOST, credentials=credentials)
    connection = BlockingConnection(parameters)
    channel = connection.channel()
    
    while True:
        co2_level = input("Enter CO2 level: ")
        
        # Create message 
        message = {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "co2": co2_level
        }
        
        message_json = json.dumps(message)
        
        channel.basic_publish(
            exchange=EXCHANGE_NAME,
            routing_key=ROUTING_KEY,
            body=message_json
        )
        
    connection.close()