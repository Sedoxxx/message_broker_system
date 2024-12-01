import requests
import json

# REST API URL
API_URL = "http://localhost:5000/message"

def main():
    print("Message Sender Test Script")

    while True:
        try:
            # Input alias and message text
            alias = input("Enter Alias: ").strip()
            text = input("Enter Message: ").strip()

            # Construct the payload
            payload = {"user_alias": alias, "message_text": text}

            # Send POST request to the REST API
            response = requests.post(API_URL, json=payload)

            # Print the response
            if response.status_code == 200:
                print("Response: ", response.json())
            else:
                print(f"Failed to send message. Status Code: {response.status_code}")
                print("Response Text: ", response.text)
            
            print("-" * 40)

        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            print("-" * 40)

if __name__ == "__main__":
    main()
