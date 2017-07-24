#!/usr/bin/python
# -*- coding: cp949 -*-

import sys
import pymysql
import redis
import time
import config_lib

# key | code | date | open | close | high | low | volum

class SixPriceMeans:

   def __init__(self):
      self.allOut = []
      conf = config_lib.CaBeConfig()
      price_means_out_path = '%s/5priceMeans.dat' % conf.get_outpath()
      self.fp = open(price_means_out_path, 'w')
      print 'init 5 PriceMeans'
   
   def find(self, lastDate, dataAll):
      print 'Start 5 PriceMeans...'
      for key, lists in dataAll.items():

         for nIndex in range(0, 20):
 
            n20 = 0.0
            fvalue = 0.0
            nbong = 0
            nSkipCount = 0
            moveLastWorkDay = ""
            total_bong = len(lists)

            for items in lists:
               if nSkipCount < nIndex:
                  nSkipCount += 1
                  continue

               fields = items.split('|')

               if nbong == 0:
                  moveLastWorkDay    = str(fields[2].strip())

               nbong += 1

               if nbong <= 20 and total_bong >= 20:
                  #fvalue = (int(fields[3]) + int(fields[4]) + int(fields[5]) + int(fields[6])) / 4.0
                  #fvalue = (int(fields[4]) + int(fields[5]) + int(fields[6])) / 3.0
                  #n20 += fvalue
                  n20 += float(fields[4]) # Close
                  if nbong == 20:
                     buf = '%s_%s|%f\n' % (fields[1], moveLastWorkDay, n20 / 20)
                     self.allOut.append(buf.strip())
                     self.fp.write(buf)
                     #print '[7 price means] %s_%s [%f] ' % (fields[1], moveLastWorkDay, n20 / 20)
              
               if nbong > 21:
                  break

            #buf = '%s|%d|%d|%d|%d|%d|%d\n' % (key, nMeans5, n4total, nMeans20, n19total, nMeans60, n59total)
            #self.fp.write(buf)
            #print 'code[%s], 5[%d] 5b[%d] 20[%d] 20b[%d] 60[%d] 60b[%d]' % (key, nMeans5, n4total, nMeans20, n19total, nMeans60, n59total)

      self.fp.close()
      
      return self.allOut

# end

