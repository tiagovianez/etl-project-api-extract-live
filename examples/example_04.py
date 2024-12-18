import requests
import json

url = "https://api.openai.com/v1/chat/completions"


headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer XXXXX"
}

data = {
    "model": "gpt-3.5-turbo",
    "messages": [{"role": "user", "content": "What is Data Engineering"}]
}

response = requests.post(url, headers=headers, data=json.dumps(data))

print(response.status_code)