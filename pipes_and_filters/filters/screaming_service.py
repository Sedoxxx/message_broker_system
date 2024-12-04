import threading

def screaming_service(input_queue, output_queue):
    while True:
        message = input_queue.get()
        if message is None:
            output_queue.put(None)
            break
        message_text = message['message_text'].upper()
        message['message_text'] = message_text
        print(f"Screaming Service: Converted message: {message}", flush=True)
        output_queue.put(message)

def start_screaming_service(input_queue, output_queue):
    screaming_thread = threading.Thread(target=screaming_service, args=(input_queue, output_queue))
    screaming_thread.start()
    return screaming_thread
