from flask import Flask, request, jsonify
import pika
import os
import time
import ast

app = Flask(__name__)

# RabbitMQ connection parameters
rabbitmq_host = os.environ.get('RABBITMQ_HOST', 'rabbitmq')
rabbitmq_port = int(os.environ.get('RABBITMQ_PORT', 5672))
rabbitmq_user = os.environ.get('RABBITMQ_DEFAULT_USER', 'guest')
rabbitmq_pass = os.environ.get('RABBITMQ_DEFAULT_PASS', 'guest')

credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_pass)
parameters = pika.ConnectionParameters(
    host=rabbitmq_host, port=rabbitmq_port, credentials=credentials
)

def connect_to_rabbitmq():
    while True:
        try:
            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()
            channel.queue_declare(queue='filter_queue', durable=True)
            print("API Service: Connected to RabbitMQ")
            return connection, channel
        except pika.exceptions.AMQPConnectionError:
            print("API Service: Failed to connect to RabbitMQ, retrying in 5 seconds...")
            time.sleep(5)

def publish_message(channel, message):
    try:
        channel.basic_publish(
            exchange='',
            routing_key='filter_queue',
            body=str(message),
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            ))
    except pika.exceptions.AMQPConnectionError:
        print("API Service: Connection lost while publishing, reconnecting...")
        connection, channel = connect_to_rabbitmq()
        publish_message(channel, message)

@app.route('/message', methods=['POST'])
def receive_message():
    data = request.get_json()
    user_alias = data.get('user_alias')
    message_text = data.get('message_text')

    if not user_alias or not message_text:
        return jsonify({'error': 'user_alias and message_text are required'}), 400

    message = {
        'user_alias': user_alias,
        'message_text': message_text
    }
    print("Received message:", message, flush=True)

    # Publish message
    publish_message(channel, message)

    return jsonify({'status': 'Message received'}), 200

if __name__ == '__main__':
    connection, channel = connect_to_rabbitmq()
    app.run(host='0.0.0.0', port=5000, debug=True)
