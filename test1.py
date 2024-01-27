import requests

def shorten_url(original_url):
    api_url = "https://is.gd/create.php"
    params = {"format": "simple", "url": original_url}

    try:
        response = requests.get(api_url, params=params)
        if response.status_code == 200:
            shortened_url = response.text.strip()
            return shortened_url
        else:
            print(f"Error {response.status_code}: {response.text}")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")

# Пример использования:
original_url = input('Введи URL ➤ ')
shortened_url = shorten_url(original_url)

if shortened_url:
    print(f"Original URL: {original_url}")
    print(f"Shortened URL: {shortened_url.replace('https://', '')}")
    print(f"{original_url}@{shortened_url.replace('https://', '')}")
