import requests

def shorten_url(original_url):
    api_url = "https://is.gd/create.php"
    cleaned_url = original_url.rstrip('/')
    params = {"format": "simple", "url": cleaned_url}

    try:
        response = requests.get(api_url, params=params)
        if response.status_code == 200:
            shortened_url = response.text.strip()
            return cleaned_url, shortened_url
        else:
            print(f"Error {response.status_code}: {response.text}")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")

# Пример использования:
original_url = "https://www.example.com/"
cleaned_url, shortened_url = shorten_url(original_url)

if shortened_url:
    print(f"")
    print(f"{cleaned_url}@{shortened_url.replace('https://', '')}")
