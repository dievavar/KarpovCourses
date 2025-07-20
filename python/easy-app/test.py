import requests

url = "http://localhost:8000/user/205/"

response = requests.post(url)
print(response.text)
