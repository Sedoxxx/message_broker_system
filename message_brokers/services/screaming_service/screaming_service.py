import pika
import os
import ast
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

def connect_and_consume():
    while True:
        try:
            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()
            channel.queue_declare(queue='screaming_queue', durable=True)
            channel.queue_declare(queue='publish_queue', durable=True)

            def callback(ch, method, properties, body):
                message = ast.literal_eval(body.decode())
                print(f"Screaming Service: Received message: {message}", flush=True)
                message_text = message['message_text'].upper()
                message['message_text'] = message_text
                print(f"Screaming Service: Screaming message: {message}", flush=True)

                try:
                    channel.basic_publish(
                        exchange='',
                        routing_key='publish_queue',
                        body=str(message),
                        properties=pika.BasicProperties(
                            delivery_mode=2,
                        ))
                except pika.exceptions.AMQPConnectionError:
                    print("Screaming Service: Connection lost while publishing, reconnecting...")
                    raise pika.exceptions.AMQPConnectionError

                ch.basic_ack(delivery_tag=method.delivery_tag)

            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(queue='screaming_queue', on_message_callback=callback)

            print('Screaming Service is running...')
            channel.start_consuming()

        except pika.exceptions.AMQPConnectionError:
            print("Screaming Service: Connection lost, retrying in 5 seconds...")
            time.sleep(5)
        except Exception as e:
            print(f"Screaming Service: Unexpected error: {e}")
            time.sleep(5)
        finally:
            try:
                channel.stop_consuming()
            except:
                pass
            try:
                connection.close()
            except:
                pass

if __name__ == '__main__':
    connect_and_consume()
