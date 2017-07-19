#!/usr/bin/python
# -*- coding: cp949 -*-

import sys
import pymysql
import redis
import time
import config_lib

# key | code | date | open | close | high | low | volum

class HighValue:

   def __init__(self):
      self.allOut = []
      conf = config_lib.CaBeConfig()
      high_price_path = '%s/HighPrice.dat' % conf.get_outpath() 
      self.fpHighPrice = open(high_price_path, 'w')
      print 'init HighValue'


   def __del__(self):
      self.fpHighPrice.close()
      print 'HighValue :: __del__'
   

   def find(self, maxBong, dataAll):

      for key, value in dataAll.items():

         per = 0.0
         nbong = 0
         tomo_date = ""
         tomo_close = 0.0
         #print 'code [%s]' % key

         for items in value:
            fields = items.split('|')
            #print 'code [%s], date[%s]' % (fields[1], fields[2])
            if nbong > 0:
               per = ((tomo_close / float(fields[3])) - 1.0) * 100.0
               if per >= 15:
                  buf = '%s|%f\n' % (fields[1], per)
                  self.allOut.append(buf.strip())
                  self.fpHighPrice.write(buf)
                  #print '[HighPrice] [%s] -> %0.2f [%d] [%d]' % (tomo_date, per, tomo_close, int(fields[3]))
               
            nbong += 1 
            tomo_close = float(fields[3])
            tomo_date  = fields[2]
            if nbong > maxBong:
               break

            #print '[%s] [%s]' % (key, items)

      print '[High Value] %s' % str(self.allOut)
      return self.allOut
          
# end
