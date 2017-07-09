#!/usr/bin/python
# -*- coding: cp949 -*-

import sys
import pymysql
import redis
import time

# key | code | date | open | close | high | low | volum

class HighValue:

   def __init__(self):
      print 'init HighValue'
   
   def find(self, maxBong, dataAll):
      for key, value in dataAll.items():

         print 'code [%s]' % key
         per = 0.0
         nbong = 0
         tomo_close = 0.0
         tomo_date = ""

         for items in value:
            fields = items.split('|')
            #print 'code [%s], date[%s]' % (fields[1], fields[2])
            if nbong > 0:
               per = ((tomo_close / float(fields[3])) - 1.0) * 100.0
               if per > 15:
                  print '[%s] -> %0.2f [%d] [%d]' % (tomo_date, per, tomo_close, int(fields[3]))
               
            nbong += 1 
            tomo_close = float(fields[3])
            tomo_date  = fields[2]
            if nbong > maxBong:
               break

            #print '[%s] [%s]' % (key, items)
          

