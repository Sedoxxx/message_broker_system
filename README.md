# Message Broker System with Pipes-and-Filters

## Introduction

This project demonstrates the implementation of a **message broker system** using RabbitMQ and its transformation into a **pipes-and-filters system**. Both versions of the system process messages through a series of stages (filters), each performing a specific task. The comparison highlights the differences in performance between the two architectures.

---

## System Architecture

The system consists of four services:

1. **API Service**: A user-facing REST API that receives POST requests containing a message and a user alias.
2. **Filter Service**: Filters out messages containing specific stop words.
3. **Screaming Service**: Converts the message text to uppercase.
4. **Publish Service**: Sends the processed message via email to a specified recipient list.

**Message Flow:**

- **RabbitMQ-Based System**:
  - The API Service receives messages and publishes them to the `filter_queue`.
  - The Filter Service consumes messages from `filter_queue`, filters out unwanted messages, and publishes valid messages to `screaming_queue`.
  - The Screaming Service consumes messages from `screaming_queue`, converts the text to uppercase, and publishes them to `publish_queue`.
  - The Publish Service consumes messages from `publish_queue` and sends emails to the recipients.

- **Pipes-and-Filters System**:
  - All services are combined into a single application. Each stage (filter) communicates via in-memory queues.

---

## Project Structure

```
message_broker_system/
├── .env
├── .env.example
├── docker-compose.yml
├── LICENSE
├── README.md
├── message_brokers/
│   ├── services/
│   │   ├── api_service/
│   │   │   ├── api_service.py
│   │   │   ├── Dockerfile
│   │   │   └── requirements.txt
│   │   ├── filter_service/
│   │   │   ├── filter_service.py
│   │   │   ├── Dockerfile
│   │   │   └── requirements.txt
│   │   ├── publish_service/
│   │   │   ├── publish_service.py
│   │   │   ├── Dockerfile
│   │   │   └── requirements.txt
│   │   └── screaming_service/
│       │   ├── screaming_service.py
│       │   ├── Dockerfile
│       │   └── requirements.txt
├── load_testing/
│   ├── load_test_pipes.py
│   ├── load_test_rabbitmq.py
│   ├── report.md
│   ├── report2.md
│   └── test.py
├── pipes_and_filters/
│   ├── filters/
│   │   ├── __pycache__/
│   │   ├── __init__.py
│   │   ├── filter_service.py
│   │   ├── publish_service.py
│   │   ├── screaming_service.py
│   ├── .env
│   ├── main.py
│   └── requirements.txt
```

---

## Prerequisites

- **Docker** and **Docker Compose** installed on your machine.
- **Python 3.7+** installed for running the load testing script.
- An SMTP server or email testing service like **Mailtrap** for sending emails.
- Optional: **cURL** or **Postman** for testing the API endpoints.

---

## Demo Video

[Demo Video Drive](https://drive.google.com/file/d/1mL-dCJAQEWZLji_5C_-AhOzaWPFDEU65/view?usp=sharing)

## Setup and Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd message_broker_system
```

### 2. Configure Environment Variables

Create a `.env` file in the root directory based on the `.env.example` file. Replace the email settings with your actual SMTP server details.

### 3. Build and Start the Services

For the **RabbitMQ-Based System**:
```bash
docker-compose up --build
```

For the **Pipes-and-Filters System**:
```bash
python main.py
```

---

## Running the Application

### Access RabbitMQ Management UI (Optional)

For the RabbitMQ-based system, you can access the RabbitMQ Management UI at [http://localhost:15672](http://localhost:15672) using the default credentials (`guest` / `guest`).

---

## Testing the Application

### Sending a Message Without Stop Words

Use `curl` or Postman to send a POST request to the API Service.

```bash
curl -X POST -H "Content-Type: application/json" \
-d '{"user_alias": "professor", "message_text": "Services should be separately deployable units!"}' \
http://localhost:5000/message
```

#### Expected Outcome

- **RabbitMQ-Based System**: The message flows through the Filter, Screaming, and Publish services, and an email is sent.
- **Pipes-and-Filters System**: The message flows through the filters in-memory, and an email is sent.

---

## Load Testing

### Running the Load Testing Scripts

Navigate to the `load_testing/` directory:

```bash
cd message_broker_system/load_testing
```

Run the load testing script for the RabbitMQ-based system:

```bash
python load_test_rabbitmq.py
```

Run the load testing script for the Pipes-and-Filters system:

```bash
python load_test_pipes.py
```

## Load Testing Performance Report

### Performance Comparison Summary

| Metric                       | RabbitMQ-Based System          | Pipes-and-Filters System          |
|------------------------------|--------------------------------|-----------------------------------|
| **Total Requests Sent**      | 50                            | 50                                |
| **Total Time Taken**         | 0.20 seconds                  | 20.55 seconds                    |
| **Requests per Second**      | 250.04                        | 2.43                              |
| **Overhead**                 | Network + broker communication | Minimal (in-memory only)         |

1. **Throughput**: The RabbitMQ-based system handles requests much faster (250.04 requests/second) due to its distributed, asynchronous nature. The Pipes-and-Filters system is limited by in-memory queues and single-process threading.
2. **Latency**: The Pipes-and-Filters system has higher latency due to sequential processing, while RabbitMQ benefits from parallelism and queuing.
3. **Scalability**: The RabbitMQ-based system supports horizontal scaling, making it more suitable for large-scale, distributed applications.

### Conclusion
The RabbitMQ-based system excels in distributed and asynchronous workloads, while the Pipes-and-Filters system is better suited for small-scale, high-performance, CPU-intensive tasks.

---

## Troubleshooting

- **RabbitMQ Connection Issues**: Ensure that the RabbitMQ service is running and accessible. The services are configured to retry connections if they fail.
- **Email Sending Issues**: Verify your SMTP server settings and credentials in the `.env` file.
- **Port Conflicts**: Ensure that the ports defined in `docker-compose.yml` are not in use by other applications.

---






