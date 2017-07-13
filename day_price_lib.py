#!/usr/bin/python
# -*- coding: cp949 -*-

import sys
import pymysql
import redis
import time
import config_lib

# key | code | date | open | close | high | low | volum

class DayPrice:

   def __init__(self):
      conf = config_lib.CaBeConfig()
      file_path = '%s/dayPrice.dat' % conf.get_outpath() 
      self.fpOut = open(file_path, 'w')
      print '__init__ DayPrice'


   def __del__(self):
      self.fpOut.close()
      print 'DayPrice :: __del__'
   

   def find(self, maxBong, dataAll):
      for key, value in dataAll.items():

         #print 'code [%s]' % key
         nBong = 0

         for items in value:
            fields = items.split('|')
            nOpen   = int(fields[3])
            nClose  = int(fields[4])
            nHigh   = int(fields[5])
            nLow    = int(fields[6])
            scode   = str(fields[1])

            nBong += 1 

            if nBong > 0:
               break

         buf = '%s|%d|%d|%d|%d\n' % (scode, nBong)
         self.fpOut.write(buf)
         print '[DayPrice] [%s] [%s]' % (scode, buf)
          
#end 
