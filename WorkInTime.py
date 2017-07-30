from datetime import *
import calendar
from datetime import datetime,timedelta
import time
#timeBucket=[[时间起，时间止]，[时间点]*2]
#从小到大排序，不支持跨日
class WorkInTime():
    def __init__(self, timeBucket, relaxTime=60, addTime=4.6, weekday='All'):    #工作时间段和冗余时间,run weekday
        self.__time = timeBucket
        self.__weekday = weekday
        now = datetime.now()
        self.__timeType = [[time.mktime(time.strptime(str(now.year) + '-' + str(now.month) + '-' + str(now.day) +\
                            ' ' + i + ':00', '%Y-%m-%d %H:%M:%S')) for i in timeB] for timeB in self.__time[:]
                         ]

        self.__timeType233 = [[i for i in timeB] for timeB in self.__time[:]
                         ]
        self.__addTime = addTime      #冗余时间
        self.__relaxTime = relaxTime    #休息时间
        self.__newday = True
        self.__today = date.today()

    def changeRelaxTime(self, relaxTime):
        self.__relaxTime = relaxTime    #休息时间

    def __resetTime(self):
        now = datetime.now()
        self.__today = date.today()
        self.__timeType = [[time.mktime(time.strptime(str(now.year) + '-' + str(now.month) + '-' + str(now.day) +\
                            ' ' + i + ':00', '%Y-%m-%d %H:%M:%S')) for i in timeB] for timeB in self.__time[:]
                         ]
    def relaxDay(self):
        #print(self.__today.weekday())
        if self.__weekday == 'All':
            return
        while str(self.__today.weekday()) not in self.__weekday:
            now = datetime.now()
            dayEnd = time.mktime(time.strptime(str(now.year) + '-' + str(now.month) + '-' + str(now.day) +\
                                            ' 23:59:59', '%Y-%m-%d %H:%M:%S'))
            sleepTime = round(dayEnd - time.time())
            #print('sleepTime' + str(sleepTime))
            #print('timeNow' + time.strftime('%H:%M:%S',time.localtime(time.time())))
            time.sleep(sleepTime+self.__addTime)
            self.__resetTime()

    # timeTrade = [['9:29', '11:30'], ['13:00', '15:00']]
    def relax(self):
        self.relaxDay()  #relaxDay
        if self.isNewDay():
            self.__resetTime()
        timeNow = time.time()
        timeBucket = self.__timeType
        if (timeNow > timeBucket[-1][-1]):      #大于一天终止时间
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
'''
wt = WorkInTime([['12:00', '12:00']], weekday='3')
wt.relaxDay()
print('3')
wt = WorkInTime([['12:00', '12:00']], weekday='2,3')
wt.relaxDay()
print('2,3')
wt = WorkInTime([['12:00', '12:00']])
wt.relaxDay()
print('')
'''
