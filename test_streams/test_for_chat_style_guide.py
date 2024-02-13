import requests

# Replace with the appropriate URL where your FastAPI server is running
# host="54.174.77.47"
host ="localhost:8000"
api_url = f"http://{host}/api/v1/chat/styled/stream"

# Replace with your actual prompt
prompt_data = {
    "sender_id": "1",
    "conversation_id": "1",
    "prompt": "What is Digitization?",
    "use_history": True
}

try:
    response = requests.post(
        api_url,
        json=prompt_data,
        stream=True,
        headers={"accept": "application/json"},
    )

    if response.status_code == 200:
        for chunk in response.iter_content():
            if chunk:
                try:
                    print(str(chunk, encoding="utf-8"), end="")
                except Exception as e:
                    pass
    else:
        print(f"Error: {response.status_code}\n{response.text}")

except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
