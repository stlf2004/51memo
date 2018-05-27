#!/usr/bin/env python
# encoding: utf-8
# Author: Johnny Loo
# Email: johnnyloo1985@gmail.com

from datetime import datetime
from dateutil.relativedelta import relativedelta
from dateutil.rrule import *
from dateutil.parser import parse
import re


class MemoTime:
    """时间关键词与时间格式化字符串的对应关系"""

    kwdb = (
        '今天中午',
        '今天晚上',
        '今天早上',
        '今天',
        '明天早上',
        '明天中午',
        '明天晚上'
        '明天',
        '后天早上',
        '后天中午',
        '后天晚上',
        '后天',
        '大后天',
        '周一',
        '周二',
        '周三',
        '周四',
        '周五',
        '周六',
        '周末',
        '周日',
        '下下周',
        '下周一',
        '下周二',
        '下周三',
        '下周四',
        '下周五',
        '下周六',
        '下周末',
        '下周日',
        '下周',
        '月初',
        '月底',
        '下下个月',
        '下个月初',
        '下个月底',
        '下个月',
        '3个月后',
        '半年后',
        '明年'
    )

    def __init__(self, timeWord):
        self.timeWord = timeWord
        self.timeFmt = '%Y-%m-%d %H:%M'
        self.timeFmted = self.getTimeFmted()

    @staticmethod
    def en2cn(s):
        """英文时间字符串转中文"""
        if re.match(r'\d{4}-\d{1,2}-\d{1,2} \d{2}:\d{2}', s):
            return s.replace('-', '年', 1).replace('-', '月', 1).replace(' ', '日', 1)

    def getTimeFmted(self):  # 进一步完善时间提取功能
        now = datetime.now()
        if self.timeWord == '今天中午':
            return MemoTime.en2cn(datetime(now.year, now.month, now.day, 12).strftime(self.timeFmt))
        elif self.timeWord == '今天晚上':
            return MemoTime.en2cn(datetime(now.year, now.month, now.day, 20).strftime(self.timeFmt))
        elif self.timeWord == '今天早上':
            return MemoTime.en2cn(datetime(now.year, now.month, now.day, 8).strftime(self.timeFmt))
        elif self.timeWord == '今天':
            return MemoTime.en2cn(now.strftime(self.timeFmt))
        elif self.timeWord == '明天早上':
            return MemoTime.en2cn((now + relativedelta(days=+1, hour=8)).strftime(self.timeFmt))
        elif self.timeWord == '明天中午':
            return MemoTime.en2cn((now + relativedelta(days=+1, hour=12)).strftime(self.timeFmt))
        elif self.timeWord == '明天晚上':
            return MemoTime.en2cn((now + relativedelta(days=+1, hour=20)).strftime(self.timeFmt))
        elif self.timeWord == '明天':
            return MemoTime.en2cn((now + relativedelta(days=+1)).strftime(self.timeFmt))
        elif self.timeWord == '后天早上':
            return MemoTime.en2cn((now + relativedelta(days=+2, hour=8)).strftime(self.timeFmt))
        elif self.timeWord == '后天中午':
            return MemoTime.en2cn((now + relativedelta(days=+2, hour=12)).strftime(self.timeFmt))
        elif self.timeWord == '后天晚上':
            return MemoTime.en2cn((now + relativedelta(days=+2, hour=20)).strftime(self.timeFmt))
        elif self.timeWord == '后天':
            return MemoTime.en2cn((now + relativedelta(days=+2)).strftime(self.timeFmt))
        elif self.timeWord == '大后天':
            return MemoTime.en2cn((now + relativedelta(days=+3)).strftime(self.timeFmt))
        elif self.timeWord == '下下周':
            return MemoTime.en2cn((now + relativedelta(weeks=+2)).strftime(self.timeFmt))
        elif self.timeWord == '周一':
            return MemoTime.en2cn((now + relativedelta(weekday=MO)).strftime(self.timeFmt))
        elif self.timeWord == '周二':
            return MemoTime.en2cn((now + relativedelta(weekday=TU)).strftime(self.timeFmt))
        elif self.timeWord == '周三':
            return MemoTime.en2cn((now + relativedelta(weekday=WE)).strftime(self.timeFmt))
        elif self.timeWord == '周四':
            return MemoTime.en2cn((now + relativedelta(weekday=TH)).strftime(self.timeFmt))
        elif self.timeWord == '周五':
            return MemoTime.en2cn((now + relativedelta(weekday=FR)).strftime(self.timeFmt))
        elif self.timeWord == '周六' or self.timeWord == '周末':
            return MemoTime.en2cn((now + relativedelta(weekday=SA)).strftime(self.timeFmt))
        elif self.timeWord == '周日':
            return MemoTime.en2cn((now + relativedelta(weekday=SU)).strftime(self.timeFmt))
        elif self.timeWord == '下下周':
            return MemoTime.en2cn((now + relativedelta(weeks=+2)).strftime(self.timeFmt))
        elif self.timeWord == '下周一':
            return MemoTime.en2cn((now + relativedelta(weeks=+1, weekday=MO)).strftime(self.timeFmt))
        elif self.timeWord == '下周二':
            return MemoTime.en2cn((now + relativedelta(weeks=+1, weekday=TU)).strftime(self.timeFmt))
        elif self.timeWord == '下周三':
            return MemoTime.en2cn((now + relativedelta(weeks=+1, weekday=WE)).strftime(self.timeFmt))
        elif self.timeWord == '下周四':
            return MemoTime.en2cn((now + relativedelta(weeks=+1, weekday=TH)).strftime(self.timeFmt))
        elif self.timeWord == '下周五':
            return MemoTime.en2cn((now + relativedelta(weeks=+1, weekday=FR)).strftime(self.timeFmt))
        elif self.timeWord == '下周六' or self.timeWord == '下周末':
            return MemoTime.en2cn((now + relativedelta(weeks=+1, weekday=SA)).strftime(self.timeFmt))
        elif self.timeWord == '下周日':
            return MemoTime.en2cn((now + relativedelta(weeks=+1, weekday=SU)).strftime(self.timeFmt))
        elif self.timeWord == '下周':
            return MemoTime.en2cn((now + relativedelta(weeks=+1)).strftime(self.timeFmt))
        elif self.timeWord == '月初':
            return MemoTime.en2cn((now + relativedelta(day=1)).strftime(self.timeFmt))
        elif self.timeWord == '月底':
            return MemoTime.en2cn((now + relativedelta(day=31)).strftime(self.timeFmt))
        elif self.timeWord == '下下个月':
            return MemoTime.en2cn((now + relativedelta(months=+2)).strftime(self.timeFmt))
        elif self.timeWord == '下个月初':
            return MemoTime.en2cn((now + relativedelta(months=+1, day=1)).strftime(self.timeFmt))
        elif self.timeWord == '下个月底':
            return MemoTime.en2cn((now + relativedelta(months=+1, day=31)).strftime(self.timeFmt))
        elif self.timeWord == '下个月':
            return MemoTime.en2cn((now + relativedelta(months=+1)).strftime(self.timeFmt))
        elif self.timeWord == '3个月后':
            return MemoTime.en2cn((now + relativedelta(months=+3)).strftime(self.timeFmt))
        elif self.timeWord == '半年后':
            return MemoTime.en2cn((now + relativedelta(months=+6)).strftime(self.timeFmt))
        elif self.timeWord == '明年':
            return MemoTime.en2cn((now + relativedelta(years=+1)).strftime(self.timeFmt))


    @classmethod
    def extractTime(cls, entry):
        """提取时间"""
        memoDate = ''
        for w in cls.kwdb:
            findResult = entry.find(w)
            if findResult != -1:
                memoDate = cls(w).timeFmted
                break
        if memoDate:
            return  memoDate
        else:
            return cls('明天').timeFmted



def main():
    print(MemoTime.extractTime('明天去上班'))

if __name__ == '__main__':
    main()