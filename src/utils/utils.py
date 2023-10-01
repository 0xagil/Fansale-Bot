import datetime

def isNowInTimePeriod(startTime, endTime): 
    now_time = datetime.datetime.now().time()
    if startTime < endTime: 
        return now_time >= startTime and now_time <= endTime 
    else: 
        return now_time >= startTime or now_time <= endTime 