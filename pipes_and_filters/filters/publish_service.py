import threading
import os
import smtplib
from email.mime.text import MIMEText

def publish_service(input_queue):
    # Email settings
    email_host = os.environ.get('EMAIL_HOST')
    email_port = int(os.environ.get('EMAIL_PORT', '25'))
    email_user = os.environ.get('EMAIL_USER')
    email_pass = os.environ.get('EMAIL_PASS')
    email_from = os.environ.get('EMAIL_FROM')
    email_to = os.environ.get('EMAIL_TO')

    while True:
        message = input_queue.get()
        if message is None:
            break
        user_alias = message['user_alias']
        message_text = message['message_text']
        print(f"Publish Service: Sending email for message: {message_text}", flush=True)
        send_email(user_alias, message_text, email_host, email_port, email_user, email_pass, email_from, email_to)

def send_email(user_alias, message_text, email_host, email_port, email_user, email_pass, email_from, email_to):
    subject = f'New Message from {user_alias}'
    body = f"From user: {user_alias}\nMessage: {message_text}"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = email_from
    msg['To'] = email_to

    try:
        with smtplib.SMTP(email_host, email_port) as server:
            server.ehlo()
            server.starttls()
            server.login(email_user, email_pass)
            server.sendmail(email_from, email_to.split(','), msg.as_string())
        print(f"Publish Service: Email sent for message: {message_text}", flush=True)
    except Exception as e:
        print(f"Publish Service: Failed to send email: {e}", flush=True)

def start_publish_service(input_queue):
    publish_thread = threading.Thread(target=publish_service, args=(input_queue,))
    publish_thread.start()
    return publish_thread
