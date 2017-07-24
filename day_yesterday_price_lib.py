#!/usr/bin/python
# -*- coding: cp949 -*-

import sys
import pymysql
import redis
import time
import config_lib

# key | code | date | open | close | high | low | volum

class YesterdayPrice:

   def __init__(self):
      print '__init__ YesterdayPrice'
      conf = config_lib.CaBeConfig()
      price_yesterday_out_path = '%s/price_yesterday.dat' % conf.get_outpath()
      self.fp = open(price_yesterday_out_path, 'w')

   def __del__(self):
      print '__del__ YesterdayPrice'
      self.fp.close()
   
   def find(self, sdate, dataAll):
      ldate = long(sdate)
      for key, value in dataAll.items():

         nbong = 0

         for items in value:
            fields = items.split('|')
            if long(fields[2]) > ldate:
               continue
            
            scode  = str(fields[1])
            nOpen  = str(fields[3])
            nClose = str(fields[4])
            nHigh  = str(fields[5])
            nLow   = str(fields[6])
            nVolum = str(fields[7]).strip()

            if nbong == 0:
               buf = '%s|%s|%s|%s|%s|%s\n' % (scode, nOpen, nClose, nHigh, nLow, nVolum)
               self.fp.write(buf)
               print '[yesterday price] [%s] [%s]' % (scode, buf)
               break

            nbong += 1 

# end
