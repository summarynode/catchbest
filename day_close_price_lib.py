#!/usr/bin/python
# -*- coding: cp949 -*-

import sys
import pymysql
import redis
import time

# key | code | date | open | close | high | low | volum

class ClosePrice:

   def __init__(self):
      print 'init ClosePrice'
   
   def find(self, sdate, dataAll):
      nbong = 0
      ldate = long(sdate)
      for key, value in dataAll.items():
         for items in value:
            fields = items.split('|')
            if long(fields[2]) > ldate:
               continue

            nbong += 1 
            if nbong > 0:
               print 'close [%s] [%d] [%s]' % (fields[1], int(fields[4]), fields[2])
               break
