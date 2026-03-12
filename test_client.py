import requests

# The exact endpoint your server is listening on
url = "http://localhost:8080/api/v1/greeter/streaming_chat"

# The message we are sending to the Greeter
payload = {
    "user_message": {
        "text": "My laptop screen is broken"
    }
}

print("Connecting to Neuro SAN Greeter...\n")
print("-" * 40)

try:
    # stream=True tells Python to keep the connection open and listen for data
    response = requests.post(url, json=payload, stream=True)
    response.raise_for_status()
    
    # Print the words to the screen exactly as the server streams them back
    for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
        if chunk:
            print(chunk, end="", flush=True)
            
except requests.exceptions.ConnectionError:
    print("\nError: Could not connect. Is the Neuro SAN server running?")
except Exception as e:
    print(f"\nAn error occurred: {e}")

print("\n\n" + "-" * 40)
print("Stream complete!")