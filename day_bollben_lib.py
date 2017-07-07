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
         for nIndex in range(0,5):

            nbong = 0
            skip_count = 0
            nOpen = 0
            nClose = 0
            siLastPer = 0.0
            lastWorkDayOpen = 0
            lastWorkDayClose = 0
            lastWorkDayHigh = 0
            lastWorkDayLow = 0
            totalBong = len(lists)

            for items in lists:
               if skip_count < nIndex:
                  skip_count += 1
                  continue

               fields = items.split('|')

               if nbong == 0 and nIndex == 0:
                  nOpen  = int(fields[3])
                  nClose = int(fields[4])
                  if nOpen < nClose:
                     siLastPer = ((nClose / nOpen) - 1) * 100

               if nbong == 0:
                  lastWorkDayOpen  = int(fields[3])
                  lastWorkDayClose = int(fields[4])
                  lastWorkDayHigh  = int(fields[5])
                  lastWorkDayLow   = int(fields[6])
                  #print 'code [%s], date[%s], Open[%d], Close[%d]' % (fields[1], fields[2], lastWorkDayOpen, lastWorkDayClose)
                   
               nbong += 1

               if nbong <= 20 and totalBong >= 20:
                  lnTmp = (stockInfo.getEndV - gPriceMeans(nArrIndex).nMeansArr20(nIndex)) ^ 2

      self.fpPriceMeans.close()
      self.fpBollBen.close()

# end

