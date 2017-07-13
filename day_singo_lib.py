#!/usr/bin/python
# -*- coding: cp949 -*-

import sys
import pymysql
import redis
import time
import config_lib

# key | code | date | open | close | high | low | volum

class Singo:

   def __init__(self):
      conf = config_lib.CaBeConfig()
      file_path = '%s/singo.dat' % conf.get_outpath() 
      self.fpOut = open(file_path, 'w')
      print '__init__ Singo'


   def __del__(self):
      self.fpOut.close()
      print 'Singo :: __del__'
   

   def find(self, maxBong, dataAll):
      for key, value in dataAll.items():

         #print 'code [%s]' % key
         nBong = 0
         nTodayPrice = 0
         curDate = ""
         scode = ""

         for items in value:
            fields = items.split('|')
            nOpen   = float(fields[3])
            nClose  = float(fields[4])

            #print 'code [%s], date[%s]' % (fields[1], fields[2])

            if nBong == 0:
               scode   = fields[1]
               curDate = fields[2]
               nTodayPrice = nClose

            if nBong > 0 and nClose > nTodayPrice:
               break

            nBong += 1 

         buf = '%s|%d\n' % (scode, nBong)
         self.fpOut.write(buf)
         print '[Singo] [%s] [%d]' % (scode, nBong)
          
#end 
