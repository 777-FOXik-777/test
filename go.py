import datetime, time, os


while True:
    now = datetime.datetime.now()
    os.system('clear')
    print (now.strftime("%d-%m-%Y %H:%M"))
    time.sleep(3)
