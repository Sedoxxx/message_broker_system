import threading

stop_words = ['bird-watching', 'ailurophobia', 'mango']

def filter_service(input_queue, output_queue):
    while True:
        message = input_queue.get()
        if message is None:
            output_queue.put(None)
            break
        message_text = message['message_text']
        if any(stop_word in message_text for stop_word in stop_words):
            print(f"Filter Service: Message filtered out due to stop words: {message_text}", flush=True)
        else:
            print(f"Filter Service: Passing message: {message}", flush=True)
            output_queue.put(message)

def start_filter_service(input_queue, output_queue):
    filter_thread = threading.Thread(target=filter_service, args=(input_queue, output_queue))
    filter_thread.start()
    return filter_thread
