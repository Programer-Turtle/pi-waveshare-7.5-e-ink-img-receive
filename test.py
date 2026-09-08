import requests

url = "http://pi5.local:5050/upload"

with open("Convert HEIC to JPG 7499.jpg", "rb") as file:
    response = requests.post(
        url,
        files={"photo": file}
    )

print(response.status_code)
print(response.json())