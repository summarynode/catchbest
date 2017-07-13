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
         pPer = 0.0
         n0BongClose = 0
         n1BongClose = 0
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

            if nBong == 1:
               if nOpen <= nClose:
                  break
               else:
                  n1BongClose = nClose

            if nBong == 2:
               if nOpen <= nClose:
                  break
               else:
                  pPer = ((n0BongClose / n1BongClose) - 1) * 100
                  buf = '%s|%s|%f\n' % (fields[1], curDate, pPer)
                  self.fpOut.write(buf)

                  print '[umyangyang] [%s] per[%f] date[%s]' % (fields[1], pPer,  fields[2])
               
            nBong += 1 

            if nBong > 3:
               break

            #print '[%s] [%s]' % (key, items)
          
#end 
