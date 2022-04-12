import datetime, time, os

now = datetime.datetime.now()

while True:
    os.system('clear')
    print (now.strftime("%d-%m-%Y %H:%M"))
    time.sleep(3)
