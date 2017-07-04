#!/usr/bin/python
# -*- coding: cp949 -*-

import sys
import pymysql
import redis
import time


class BunService:

   allData = {}

   def __init__(self):
      print '__init__'
   
   def cprint(self, num):
      print 'add [%d]' % num

   def loading(self, sdate):
      filepath = '/home/erpy/catch_best/2bunbong-price-%s.log.sort' % sdate
      print 'filepath [%s]' % filepath

      bOut = False
      total = 0
      f = open(filepath, 'r')
      while True:
         if bOut: break;
         aft_code = ""
         bun_list = []
         while True:
            last_pos = f.tell()
            line = f.readline().strip()
            if not line: 
               bOut = True
               break

            items = line.split('|') 
            if len(items) != 7:
               continue

            #print 'line [%s]' % line
            s_code = items[0]
            if len(aft_code) != 0:
               if s_code != aft_code:
                  BunService.allData[aft_code] = bun_list
                  f.seek(last_pos)
                  #print 'allDict size [%d] [%d]' % (len(DayService.allData), len(day_list))
                  break

            bun_list.append(line)
            aft_code = s_code


      f.close()

      return BunService.allData
      
