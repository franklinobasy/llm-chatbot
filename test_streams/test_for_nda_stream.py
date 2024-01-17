import requests

# Replace with the appropriate URL where your FastAPI server is running
host="54.174.77.47"
# host ="localhost:8000"
api_url = f"http://{host}/api/v1/NDA/generate/stream"

# Replace with your actual prompt
prompt_data = {
  "answers": [
    "", "", "", "", ""
  ]
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


