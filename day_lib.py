#!/usr/bin/python
# -*- coding: cp949 -*-

import sys
import pymysql
import redis
import time
import config_lib

class DayService:

   allData = {}

   def __init__(self):
      print '__init__'
   
   def cprint(self, num):
      print 'add [%d]' % num

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
      
