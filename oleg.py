import requests

def send_sms_request(phone_number):
    url = "http://my.telegram.org/auth/send_code"
    data = {"phone": phone_number}
    response = requests.post(url, data=data)
    return response

if __name__ == "__main__":
    phone_number = "380638966197"
    response = send_sms_request(phone_number)
    print(response)