#!/usr/bin/python
# -*- coding: cp949 -*-

import sys
import pymysql
import redis
import time
import config_lib

# key | code | date | open | close | high | low | volum

class Umumyang5Surpass:

   def __init__(self):
      conf = config_lib.CaBeConfig()
      file_path = '%s/umumyang5surpass.dat' % conf.get_outpath() 
      self.fpOut = open(file_path, 'w')
      print 'init Umumyang5Surpass'


   def __del__(self):
      self.fpOut.close()
      print 'HighValue :: __del__'
   

   def find(self, maxBong, dataAll):
      for key, value in dataAll.items():

         #print 'code [%s]' % key
         nBong = 0
         pPer1 = 0.0
         pPer2 = 0.0
         n0BongClose = 0
         nTradeAmount0 = 0
         nTradeAmount1 = 0
         nTradeAmount2 = 0
         n1BongClose = 0
         n2BongClose = 0
         curDate = ""

         for items in value:
            fields = items.split('|')
            nOpen   = float(fields[3])
            nClose  = float(fields[4])

            #print 'code [%s], date[%s]' % (fields[1], fields[2])

            if nBong == 0:
               if nOpen >= nClose:
                  break
               else:
                  curDate = fields[2]
                  n0BongClose = nClose
                  nTradeAmount0 = int(fields[7])

            if nBong == 1:
               if nOpen >= nClose:
                  break
               else:
                  n1BongClose = nClose
                  nTradeAmount1 = int(fields[7])

            if nBong == 2:
               if nOpen <= nClose:
                  break
               else:
                  n2BongClose = nClose
                  nTradeAmount2 = int(fields[7])

                  pPer1 = ((n0BongClose / n1BongClose) - 1) * 100
                  pPer2 = ((n1BongClose / n2BongClose) - 1) * 100
                  buf = '%s|%s|%f|%f\n' % (fields[1], curDate, pPer1, pPer2)

                  if n1BongClose < n0BongClose and (pPer1 >= 3 or pPer2 >= 3):
                     #if nTradeAmount0 < nTradeAmount1:
                     self.fpOut.write(buf)
                     print '[umyangyang] [%s] per1[%f] per2[%d] date[%s]' % (fields[1], pPer1, pPer2, fields[2])
               
            nBong += 1 

            if nBong > 3:
               break

            #print '[%s] [%s]' % (key, items)
          
#end 
