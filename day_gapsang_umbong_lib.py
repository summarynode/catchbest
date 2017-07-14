#!/usr/bin/python
# -*- coding: cp949 -*-

import sys
import pymysql
import redis
import time
import config_lib

# key | code | date | open | close | high | low | volum

class GapSangUm:

   def __init__(self):
      conf = config_lib.CaBeConfig()
      file_path = '%s/gapSangUm.dat' % conf.get_outpath() 
      self.fpOut = open(file_path, 'w')
      print '__init__ GapSangUm'


   def __del__(self):
      self.fpOut.close()
      print 'GapSangUm :: __del__'
   

   def find(self, sdate, dataAll):
      nTotal = 0
      for key, value in dataAll.items():

         #print 'code [%s]' % key
         nBong = 0
         nYesterdayClose = 0
         nYesterdayOpen  = 0
         curDate = ""
         scode = ""

         for items in value:
            fields = items.split('|')
            nOpen   = float(fields[3])
            nClose  = float(fields[4])
            scode   = str(fields[1])

            if nYesterdayClose > 0:
               if nYesterdayOpen > nClose and nYesterdayOpen > nOpen and nYesterdayClose > nOpen and nYesterdayClose > nClose:
                  if nYesterdayOpen > nYesterdayClose:
                     print '[GapSangUm] [%s] [%s]' % (scode, curDate)
                     nTotal += 1

            nYesterdayClose = nClose
            nYesterdayOpen  = nOpen
            curDate = str(fields[2])

            nBong += 1

            if nBong == 2:
               break

      print '[GapSangUm] total [%d]' % (nTotal)
#end 
