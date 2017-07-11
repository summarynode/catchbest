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

         print 'code [%s]' % key
         nBong = 0
         n0BongClose = 0
         n1BongClose = 0
         curDate = ""

         for items in value:
            fields = items.split('|')
            nOpen   = float(fiedls[3])
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
               
               
            nBong += 1 

            #print '[%s] [%s]' % (key, items)
          
#end 
