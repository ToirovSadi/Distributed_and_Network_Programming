import json

from pika import BlockingConnection, ConnectionParameters, PlainCredentials

RMQ_HOST = 'localhost'
RMQ_USER = 'rabbit'
RMQ_PASS = '1234'
EXCHANGE_NAME = 'amq.topic'

if __name__ == '__main__':
    credentials = PlainCredentials(RMQ_USER, RMQ_PASS)
    parameters = ConnectionParameters(host=RMQ_HOST, credentials=credentials)
    connection = BlockingConnection(parameters)
    channel = connection.channel()
    
    while True:
        query = input("Enter Query: ")
        
        message = {
            "query": query
        }
        
        channel.basic_publish(
            exchange=EXCHANGE_NAME,
            routing_key='rep.' + query,
            body=json.dumps(message)
        )
        
    connection.close()
