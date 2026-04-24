import requests

BASE = "http://127.0.0.1:5000/"

data = [{"likes": 10, "name": "Flask Tutorial","views": 100},
        {"likes": 20, "name": "Django Tutorial","views": 200},
        {"likes": 30, "name": "FastAPI Tutorial","views": 300}]

for i in range(len(data)):
    response = requests.put(BASE + "video/" + str(i), json=  data[i])
    print("PUT:", response.json())

input()

response = requests.delete(BASE + "video/1")
print("DELETE:", response.status_code)

input()

response = requests.get(BASE + "video/6")
print("GET:", response.json())