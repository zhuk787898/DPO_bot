import requests

url = 'http://127.0.0.1:8002/generate'

# Параметры запроса
payload = {
    "photos_folder_path": "C:\DPO\ishodniki/temp_file_31.mp4"
}

# Отправка POST запроса
response = requests.post(url, json=payload)

# Вывод ответа сервера
print(response.json())