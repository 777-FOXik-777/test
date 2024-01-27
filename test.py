import time
import os
import subprocess

# Шаг 1: Скачивание страницы

# Введите URL
url = input('\nВыбери URL ➤ ')

# Используем wget для загрузки HTML-кода страницы
subprocess.run(['wget', '--recursive', '--convert-links', '--page-requisites', '--no-parent', '-nc', url])

# Ждем некоторое время перед обработкой HTML-кода
time.sleep(5)

# Ждем, пока wget завершит загрузку изображений
subprocess.run(['wget', '--wait=5', '-nc', '--recursive', '--level=1', '--no-parent', '--no-clobber', '--convert-links', '--page-requisites', url])

# Шаг 2: Запуск локального сервера

# Выполняем команду для запуска локального сервера на порту 8000 (или другом свободном порту)
local_server_command = 'python -m http.server 8000'

# Запускаем команду для локального сервера с помощью subprocess
local_server_process = subprocess.Popen(local_server_command, shell=True, stdout=subprocess.PIPE)

# Печатаем сообщение о запуске локального сервера
print("Локальный сервер запущен на порту 8000")

# Добавляем задержку, чтобы сервер успел запуститься и обработать запросы
time.sleep(5)

# Шаг 3: Запуск Serveo.net

# Используем оригинальную команду Serveo.net без изменений
tru_201 = '8000'  # Замените на нужный вам порт
serveo_command = f'ssh -R 80:localhost:{tru_201} serveo.net -T -n'
serveo_process = subprocess.Popen(serveo_command, shell=True, stdout=subprocess.PIPE)

# Получаем public URL из вывода процесса Serveo
serveo_url = serveo_process.stdout.readline().strip().decode('utf-8').split()[-1]

print(f"Приложение доступно по следующему public URL: {serveo_url}")

# Добавляем задержку, чтобы скрипт не завершался сразу
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    # Прерываем выполнение при нажатии Ctrl+C

    # Завершаем процессы локального сервера и Serveo
    local_server_process.terminate()
    serveo_process.terminate()

    print("Скрипт завершен.")
