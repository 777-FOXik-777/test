import requests
import subprocess

# 1. Скачивание веб-страницы
url = 'http://example.com'
response = requests.get(url)

if response.status_code == 200:
    # 2. Сохранение содержимого страницы в файл
    with open('downloaded_page.html', 'w', encoding='utf-8') as file:
        file.write(response.text)

    # 3. Отправка файла на удаленный сервер через SSH
    local_file_path = 'downloaded_page.html'
    remote_server = 'serveo.net'

    # Команда для SSH
    ssh_command = f'ssh -R 80:localhost:8080 {remote_server} -T -n 2>&1 | awk \'/serveo.net/ {{print $5}}\''

    # Выполнение команды через subprocess
    try:
        subprocess.run(['scp', local_file_path, f'{remote_server}:~/'])
        subprocess.run(ssh_command, shell=True)
    except Exception as e:
        print(f"Error: {e}")
else:
    print(f"Failed to download the webpage. Status code: {response.status_code}")
