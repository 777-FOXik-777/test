import datetime

now = datetime.datetime.now()

print
print ("Текущая дата и время с использованием метода str:")
print (str(now))

print (" ")
print ("Текущая дата и время с использованием атрибутов:")
print ("Текущий год: %d" % now.year)
print ("Текущий месяц: %d"% now.month)
print ("Текущий день: %d" % now.day)
print ("Текущий час: %d" % now.hour)
print ("Текущая минута: %d" % now.minute)
print ("Текущая секунда: %d" % now.second)
print ("Текущая микросекунда: %d" % now.microsecond)

print
print ("Текущая дата и время с использованием strftime:")
print (now.strftime("%d-%m-%Y %H:%M"))

print
print ("Текущая дата и время с использованием isoformat:")
print (now.isoformat())
