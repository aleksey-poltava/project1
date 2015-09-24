import datetime


i = datetime.datetime.now()
if i.hour < 9 or i.hour > 19:
    print "sleep"