import pika
import os
import ast
import smtplib
from email.mime.text import MIMEText
import time

# RabbitMQ connection parameters
rabbitmq_host = os.environ.get('RABBITMQ_HOST', 'rabbitmq')
rabbitmq_port = int(os.environ.get('RABBITMQ_PORT', 5672))
rabbitmq_user = os.environ.get('RABBITMQ_DEFAULT_USER', 'guest')
rabbitmq_pass = os.environ.get('RABBITMQ_DEFAULT_PASS', 'guest')

credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_pass)
parameters = pika.ConnectionParameters(
    host=rabbitmq_host, port=rabbitmq_port, credentials=credentials
)

# Email settings
email_host = os.environ.get('EMAIL_HOST')
email_port = int(os.environ.get('EMAIL_PORT'))
email_user = os.environ.get('EMAIL_USER')
email_pass = os.environ.get('EMAIL_PASS')
email_from = os.environ.get('EMAIL_FROM')
email_to = os.environ.get('EMAIL_TO')

def send_email(user_alias, message_text):
    subject = f'New Message from {user_alias}'
    body = f"From user: {user_alias}\nMessage: {message_text}"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = email_from
    msg['To'] = email_to

    try:
        with smtplib.SMTP(email_host, email_port) as server:
            server.starttls()
            server.login(email_user, email_pass)
            server.sendmail(email_from, email_to.split(','), msg.as_string())
        print(f"Publish Service: Email sent for message: {message_text}", flush=True)
    except Exception as e:
        print(f"Publish Service: Failed to send email: {e}", flush=True)

def connect_and_consume():
    while True:
        try:
            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()
            channel.queue_declare(queue='publish_queue', durable=True)

            def callback(ch, method, properties, body):
                message = ast.literal_eval(body.decode())
                print(f"Publish Service: Received message: {message}", flush=True)
                user_alias = message['user_alias']
                message_text = message['message_text']
                send_email(user_alias, message_text)
                ch.basic_ack(delivery_tag=method.delivery_tag)

            channel.basic_qos(prefetch_count=5)
            channel.basic_consume(queue='publish_queue', on_message_callback=callback)

            print('Publish Service is running...')
            channel.start_consuming()

        except pika.exceptions.AMQPConnectionError:
            print("Publish Service: Connection lost, retrying in 5 seconds...", flush=True)
            time.sleep(5)
        except Exception as e:
            print(f"Publish Service: Unexpected error: {e}", flush=True)
            time.sleep(5)

if __name__ == '__main__':
    connect_and_consume()
