import requests
import threading
import time
import random
import string

# Configuration
API_URL = 'http://localhost:5000/message'  # Update if the API is hosted elsewhere
NUM_THREADS = 5  # Number of concurrent threads
REQUESTS_PER_THREAD = 10  # Number of requests per thread

# Test Messages
test_messages = [
    "Services should be separately deployable units!",
    "I love microservices architecture.",
    "Event-driven systems are scalable.",
    "Let's test the system under load.",
    "Distributed systems can be complex.",
    "This message contains bird-watching.",  # Contains a stop word
    "Avoiding mango in messages.",
    "Fear of cats is called ailurophobia.",  # Contains a stop word
    "High throughput is essential.",
    "Load testing is important."
]

def send_requests(thread_id):
    for i in range(REQUESTS_PER_THREAD):
        message_text = random.choice(test_messages)
        user_alias = 'user_' + ''.join(random.choices(string.ascii_lowercase, k=5))
        data = {
            'user_alias': user_alias,
            'message_text': message_text
        }
        try:
            response = requests.post(API_URL, json=data)
            if response.status_code != 200:
                print(f"Thread {thread_id}: Received non-200 response code: {response.status_code}")
        except Exception as e:
            print(f"Thread {thread_id}: Exception occurred: {e}")
        time.sleep(0.01)  # Slight delay to simulate real-world usage

def main():
    start_time = time.time()
    threads = []

    print(f"Starting load test with {NUM_THREADS} threads, each sending {REQUESTS_PER_THREAD} requests.")

    for thread_id in range(NUM_THREADS):
        t = threading.Thread(target=send_requests, args=(thread_id,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    end_time = time.time()
    duration = end_time - start_time
    total_requests = NUM_THREADS * REQUESTS_PER_THREAD

    print(f"Load test completed.")
    print(f"Total requests sent: {total_requests}")
    print(f"Total time taken: {duration:.2f} seconds")
    print(f"Requests per second: {total_requests / duration:.2f}")

    # Write results to report.md
    with open('report2.md', 'w') as report_file:
        report_file.write('# Load Testing Report for RabbitMQ-based System\n\n')
        report_file.write(f'- **Total Requests Sent**: {total_requests}\n')
        report_file.write(f'- **Total Time Taken**: {duration:.2f} seconds\n')
        report_file.write(f'- **Requests per Second**: {total_requests / duration:.2f}\n')

if __name__ == '__main__':
    main()