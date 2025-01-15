import requests
import json

url = 'https://beetle-prompt-finally.ngrok-free.app/error/'
# headers
headers = {
	"ngrok-skip-browser-warning": "69420",
    'accept': 'application/json',
    'Content-Type': 'application/json',
    "token": "543"
}

# param
data = {
  "code": 400,
  "message": "string"
}


response = requests.post(url, headers=headers, json=data).json()
print(response)