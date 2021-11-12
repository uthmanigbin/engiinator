import requests

data = {"a_key": "a_time"}

url = "http://localhost:8080/"

response = requests.post(url, data)

print(response)
