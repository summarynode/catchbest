#!/usr/bin/python
# -*- coding: cp949 -*-

import sys
import pymysql
import redis
import time
import config_lib

# key | code | date | open | close | high | low | volum

class WeekBong:

   def __init__(self):
      self.allOut = []
      conf = config_lib.CaBeConfig()
      high_price_path = '%s/weekBong.dat' % conf.get_outpath() 
      self.fpHighPrice = open(high_price_path, 'w')
      print '__init__ WeekBong'


   def __del__(self):
      self.fpHighPrice.close()
      print '__del__ WeekBong'
   

   def find(self, maxBong, dataAll):

      for key, value in dataAll.items():

         nbong = 0
         nIndex = 0
         nFiveClose = 0

         for items in value:
            if len(value) < 100:
               break

            fields = items.split('|')
            sCode  = str(fields[1])
            sDate  = str(fields[2])
            nOpen  = int(fields[3])
            nClose = int(fields[4])
               
            if nbong > 100:
               break

            if nbong % 5 == 0:
               print '===== [%d] [%d]' % (nIndex, nFiveClose)
               nIndex = 0
               nFiveClose = 0

            nbong += 1 
            nIndex += 1

            if nIndex == 5:
               nFiveClose = nClose

            print '[%s] [%s] [%s] [%d]' % (sCode, sDate, nClose, nIndex)

      print '[WeekBong] %s' % str(self.allOut)
      return self.allOut
          
# end
