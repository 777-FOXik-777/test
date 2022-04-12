import datetime, time

now = datetime.datetime.now()

while True:
    os.system('clear')
    print (now.strftime("%d-%m-%Y %H:%M"))
    time.sleep(3)
