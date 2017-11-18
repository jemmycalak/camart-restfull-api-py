import datetime dateutil.parser
from datetime import date, time, datetime

def time_parse(myTime):
    if myTime == None:
        return myTime
    else:
        # to convert from TIMESTAMP become new format time
        myTime1 = str(dateutil.parser.parse(myTime, dayfirst=True))
        myTime2 = datetime.strptime(myTime1, '%Y-%m-%d %H:%M:%S.%f')
        newFormat = "%d-%m-%Y %H:%M:%H"
        newTime = myTime2.strftime(newFormat)
        return newTime