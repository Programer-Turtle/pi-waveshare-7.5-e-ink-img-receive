import requests

url = "http://127.0.0.1:5050/upload"

with open("test.jpg", "rb") as file:
    response = requests.post(
        url,
        files={"photo": file}
    )

print(response.status_code)
print(response.json())