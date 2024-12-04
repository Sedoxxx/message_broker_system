import queue
import threading
import signal
import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
# Import filter functions
from filters.filter_service import start_filter_service
from filters.screaming_service import start_screaming_service
from filters.publish_service import start_publish_service

# Queues to connect the pipeline stages
input_queue = queue.Queue()
filter_queue = queue.Queue()
screaming_queue = queue.Queue()

threads = []  # List to keep track of running threads

def api_service():
    app = Flask(__name__)

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
        print("API Service: Received message:", message, flush=True)

        # Put message into the input queue
        input_queue.put(message)

        return jsonify({'status': 'Message received'}), 200

    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

def signal_handler(sig, frame):
    """Gracefully handle keyboard interrupt."""
    print("\nKeyboard interrupt received. Shutting down gracefully...", flush=True)
    
    # Stop all queues by sending termination signals
    input_queue.put(None)
    filter_queue.put(None)
    screaming_queue.put(None)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    print("All services stopped. Exiting application.", flush=True)
    os._exit(0)  # Ensure complete shutdown

if __name__ == '__main__':
    # Register signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)

    # Start the filter threads and store them in the threads list
    filter_thread = start_filter_service(input_queue, filter_queue)
    screaming_thread = start_screaming_service(filter_queue, screaming_queue)
    publish_thread = start_publish_service(screaming_queue)
    threads.extend([filter_thread, screaming_thread, publish_thread])

    try:
        # Start the Flask app in the main thread
        api_service()
    except Exception as e:
        print(f"Error: {e}", flush=True)
        signal_handler(None, None)
