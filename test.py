import time
import subprocess
import os

# Шаг 1: Скачивание страницы

# Введите URL
url = input('\nВыбери URL ➤ ')

# Используем wget для загрузки HTML-кода страницы и сохранения его как index.html
subprocess.run(['wget', '--recursive', '--convert-links', '--page-requisites', '--no-parent', '--output-document=index.html', url])

# Ждем некоторое время перед обработкой HTML-кода
time.sleep(5)

# Ждем, пока wget завершит загрузку изображений
subprocess.run(['wget', '--wait=5', '-nc', '--recursive', '--level=1', '--no-parent', '--no-clobber', '--convert-links', '--page-requisites', url])

# Шаг 2: Поиск свободного порта для локального сервера

# Находим свободный порт
for port in range(8000, 8100):
    try:
        local_server_command = f'python -m http.server {port}'
        subprocess.run(local_server_command, shell=True, check=True)
        break
    except subprocess.CalledProcessError:
        continue

print(f"Локальный сервер запущен на порту {port}")

# Ждем, чтобы сервер успел запуститься и обработать запросы
time.sleep(5)

# Шаг 3: Запуск Serveo.net для тунелирования файла

# Используем оригинальную команду Serveo.net без изменений
tru_port = str(port)  # Используем тот же порт, на котором запущен локальный сервер
serveo_command = f'ssh -R 80:localhost:{tru_port} serveo.net -T -n index.html'
serveo_process = subprocess.Popen(serveo_command, shell=True, stdout=subprocess.PIPE)

# Получаем public URL из вывода процесса Serveo
serveo_url = serveo_process.stdout.readline().strip().decode('utf-8').split()[-1]

print(f"Файл index.html доступен по следующему public URL: {serveo_url}")

# Добавляем задержку, чтобы скрипт не завершался сразу
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    # Прерываем выполнение при нажатии Ctrl+C

    # Завершаем процесс Serveo
    serveo_process.terminate()

    print("Скрипт завершен.")
