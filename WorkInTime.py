from datetime import *
from datetime import datetime,timedelta
import time
#timeBucket=[[时间起，时间止]，[时间点]*2]
#从小到大排序，不支持跨日
class WorkInTime():
    def __init__(self, timeBucket, relaxTime=60, addTime=4.6):    #工作时间段和冗余时间
        self.__time = timeBucket
        now = datetime.now()
        self.__timeType = [[time.mktime(time.strptime(str(now.year) + '-' + str(now.month) + '-' + str(now.day) +\
                            ' ' + i + ':00', '%Y-%m-%d %H:%M:%S')) for i in timeB] for timeB in self.__time[:]
                         ]

        self.__timeType233 = [[i for i in timeB] for timeB in self.__time[:]
                         ]
        self.__addTime = addTime      #冗余时间
        self.__relaxTime = relaxTime    #休息时间
        self.__newday = True

    def changeRelaxTime(self, relaxTime):
        self.__relaxTime = relaxTime    #休息时间

    # timeTrade = [['9:29', '11:30'], ['13:00', '15:00']]
    def relax(self):
        timeNow = time.time()
        timeBucket = self.__timeType
        if (timeNow > timeBucket[1][-1]):      #大于一天终止时间
            sleepTime = round(timeBucket[0][0] - timeNow + 24 * 60 * 60, 0)
            #print('timeBegin:' + str(time.asctime(time.localtime(timeBucket[0][0]))))
            #print('sleepTime' + str(sleepTime))
            #print('timeNow' + time.strftime('%H:%M:%S',time.localtime(time.time())))
            if (sleepTime < 0):
                return
            time.sleep(sleepTime+self.__addTime)
            self.__newday = True
        elif timeNow < timeBucket[0][0]:      #小于一天开始时间
            sleepTime = round(timeBucket[0][0] - timeNow)
            self.__newday = True
            time.sleep(sleepTime + self.__addTime)
        else:
            self.__newday = False
            for i in range(len(timeBucket)-1)[::-1]:
                if (timeNow > timeBucket[i][1] and timeNow <= timeBucket[i+1][0]):
                    sleepTime = round(timeBucket[i+1][0]-timeNow)
                    time.sleep(sleepTime+self.__addTime)
        time.sleep(self.__relaxTime)

    def isNewDay(self):
        return self.__newday


