import requests

# Введите номер телефона
phone_number = "380638966197"

# Задайте URL-адрес и параметры запроса
url = "https://my.telegram.org/auth/send_password"
params = {
    "phone": phone_number,
}

# Отправьте запрос и получите ответ
response = requests.get(url, params=params)

# Проверьте код ответа
if response.status_code == 200:
    # SMS-код отправлен на указанный номер телефона
    print("SMS-код отправлен на номер", phone_number)
else:
    # Произошла ошибка
    print("Ошибка:", response.status_code)



# Задайте URL-адрес и параметры запроса
url = "https://zoom.us/api/v2/meetings/{}/send_sms".format(meeting_id)
params = {
    "phone_number": phone_number,
    "message": "Ваш SMS-код: 123456",
}

# Отправьте запрос и получите ответ
response = requests.post(url, params=params)

# Проверьте код ответа
if response.status_code == 200:
    # SMS-код отправлен на указанный номер телефона
    print("SMS-код отправлен на номер", phone_number)
else:
    # Произошла ошибка
    print("Ошибка:", response.status_code)
