#!/usr/bin/python
# -*- coding: cp949 -*-

import sys
import pymysql
import redis
import time

# key | code | date | open | close | high | low | volum

class BollBen:

   def __init__(self):
      self.priceMeansDic = {}
      self.fpPriceMeans = open('/Users/oj.bae/Work/catchbest/out/priceMeans.dat', 'r')
      self.fpBollBen = open('/Users/oj.bae/Work/catchbest/out/bollBen.dat', 'w')

      while True:
         line = self.fpPriceMeans.readline().strip()
         if not line:
            print 'priceMeans breaking...'
            break

         fields = line.split('|')
         if len(fields) != 7:
            print 'skip is not 7 items [%s]' % (line)
            continue

         scode = fields[0]
         print 'scode [%s] [%s]' % (scode, str(fields))

      print 'init BollBen'
   
   def find(self, lastDate, dataAll):
      print 'Start BollBen...'
      for key, lists in dataAll.items():
         nbong = 0
         for items in lists:
            fields = items.split('|')
            if nbong == 0:
               lastWorkDayOpen    = int(fields[3])
               lastWorkDayClose   = int(fields[4])
               #print 'code [%s], date[%s], Open[%d], Close[%d]' % (fields[1], fields[2], lastWorkDayOpen, lastWorkDayClose)

            nbong += 1

      self.fpPriceMeans.close()
      self.fpBollBen.close()

# end

