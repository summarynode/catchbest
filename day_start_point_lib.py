#!/usr/bin/python
# coding=utf8

import sys
import pymysql
import redis
import time

# key | code | date | open | close | high | low | volum

class StartPoint:

   def __init__(self):
      print 'init ClosePrice'
   
   def find(self, sdate, dataAll):
      ldate = long(sdate)
      for key, value in dataAll.items():

         nbong = 0
         maxVolum = 0
         nVolum = 0
         curDate = ""
         scode = ""
         spOpen = 0
         spClose = 0

         for items in value:
            fields = items.split('|')
            if long(fields[2]) > ldate:
               continue

            nVolum = int(fields[7])
            if nVolum > maxVolum:
               maxVolum = nVolum
               curDate  = fields[2]
               scode    = fields[1]
               spOpen   = int(fields[3])
               spClose  = int(fields[4])

            nbong += 1 

            if nbong >= 250:
               break

         print '[시작점] [%s] [%s] open[%d], close[%d], volum[%d]' % (scode, curDate, spOpen, spClose, maxVolum)

# end
