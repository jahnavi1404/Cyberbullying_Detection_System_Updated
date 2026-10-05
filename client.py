import requests

url = "http://127.0.0.1:5000/predict"

messages = [
    "You are so stupid",
    "can i get your phone number and address.i have been stalking you a while. please tell me",
    "Have a great day",
]

for m in messages:
    response = requests.post(url, json={"message": m})
    print(m, "->", response.json())
