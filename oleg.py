import requests

# Введите номер телефона
phone_number = "380638966197"

# Задайте URL-адрес и параметры запроса
url = "https://my.telegram.org/auth/send_password"
params = {"phone": phone_number}

# Отправьте запрос и получите ответ
response = requests.get(url, params=params)

# Проверьте код ответа
if response.ok:
    # SMS-код успешно отправлен на указанный номер телефона
    print(f"SMS-код успешно отправлен на номер {phone_number}")
else:
    # Возникла ошибка при отправке SMS-кода
    print(f"Ошибка: {response.status_code}")
