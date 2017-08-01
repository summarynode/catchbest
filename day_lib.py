#!/usr/bin/python
# -*- coding: cp949 -*-

import sys
import pymysql
import redis
import time
import config_lib
import datetime

class DayService:

   allData = {}

   def __init__(self):
      print '__init__ DayService'


   def __del__(self):
      print '__del__ DayService'


   def connectRedis(self):
      self.redi = redis.StrictRedis(host='localhost', port=7379, db=0)
      return self.redi


   def getDayName(self, y, m, d):
      dayString = ["MON", "THU","WED", "THU", "FRI", "SAT", "SUN"]
      return dayString[datetime.date(y, m, d).weekday()]


   def isExistRedis(self, key, redi):
      if len(key.strip()) == 0:
         return False

      r_value = redi.get(key)
      if r_value == None:
         return False

      if len(r_value.strip()) == 0:
         return False

      return True


   def getRedis(self, key, redi):
      if len(key.strip()) == 0:
         print 'getRedis() is key False [%s]' % str(key)
         return ""

      r_value = redi.get(key)
      
      return r_value


   def setRedis(self, key, r_value, redi):
      if len(key.strip()) == 0:
         print 'setRedis is not key'
         return False

      ret = redi.set(key, r_value)
      if ret == False:
         print 'setRedis set False key[%s] value[%s]' % (str(key), str(r_value))
         return False

      return True

   
   def loading(self, sdate):
      conf = config_lib.CaBeConfig()
      loading_day_path = '%s/1bong-price-%s.log.sort' % (conf.get_outpath(), sdate)
      print 'loading_day_path [%s]' % loading_day_path

      bOut = False
      total = 0
      f = open(loading_day_path, 'r')
      while True:
         if bOut: break;
         aft_code = ""
         day_list = []
         while True:
            last_pos = f.tell()
            line = f.readline().strip()
            if not line: 
               bOut = True
               break

            items = line.split('|') 
            if len(items) != 8:
               continue

            #print 'line [%s]' % line
            s_code = items[1]
            if len(aft_code) != 0:
               if s_code != aft_code:
                  DayService.allData[aft_code] = day_list
                  f.seek(last_pos)
                  #print 'allDict size [%d] [%d]' % (len(DayService.allData), len(day_list))
                  break

            day_list.append(line)
            aft_code = s_code


      f.close()

      return DayService.allData
      
