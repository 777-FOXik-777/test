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

