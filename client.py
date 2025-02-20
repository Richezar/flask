import requests


response = requests.post(
    "http://127.0.0.1:5000/api/v1/advertisement",
    json={"title": "PS5", "description": "sell ps5", "owner": "Ivan"},

)

print(response.status_code)
print(response.text)

response = requests.get(
    "http://127.0.0.1:5000/api/v1/advertisement/1",
    json={"title": "PS5", "description": "sell ps5", "owner": "Ivan"},

)

print(response.status_code)
print(response.text)

response = requests.delete(
    "http://127.0.0.1:5000/api/v1/advertisement/1",
    json={"title": "PS5", "description": "sell ps5", "owner": "Ivan"},

)

print(response.status_code)
print(response.text)