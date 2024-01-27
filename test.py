import requests
import subprocess
import time
from bs4 import BeautifulSoup

def download_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверка на успешный запрос
        return response.text, response.url
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при скачивании страницы: {e}")
        return None, None

def make_absolute_links(soup, base_url):
    for tag in soup.find_all(['a', 'link'], href=True):
        if not tag['href'].startswith(('http://', 'https://', '//')):
            tag['href'] = base_url + tag['href']
    for tag in soup.find_all(['img', 'script'], src=True):
        if not tag['src'].startswith(('http://', 'https://', '//')):
            tag['src'] = base_url + tag['src']
    for tag in soup.find_all('img', {'data-src': True}):
        if not tag['data-src'].startswith(('http://', 'https://', '//')):
            tag['data-src'] = base_url + tag['data-src']

def save_html_to_file(soup, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(str(soup))

def run_local_server():
    local_server_command = ['python', '-m', 'http.server', '8000']
    subprocess.run(local_server_command, check=True)

def main():
    url = input('\nВыберите URL ➤ ')
    html_content, base_url = download_page(url)

    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')

        make_absolute_links(soup, base_url)

        time.sleep(5)

        script = """
        <script>
            document.addEventListener("DOMContentLoaded", function() {
                var lazyImages = document.querySelectorAll('img[data-src]');
                lazyImages.forEach(function(img) {
                    img.setAttribute('src', img.getAttribute('data-src'));
                });
            });
        </script>
        """
        soup.body.append(BeautifulSoup(script, 'html.parser'))

        save_html_to_file(soup, 'downloaded_page.html')
        print("Страница успешно скачана и сохранена в файл downloaded_page.html")

        save_html_to_file(soup, 'index.html')
        print("Копия страницы сохранена в файл index.html")

        print("Запуск локального сервера...")
        run_local_server()

if __name__ == "__test__":
    main()
