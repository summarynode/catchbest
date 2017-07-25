#!/usr/bin/python
# -*- coding: cp949 -*-

import sys
import pymysql
import redis
import time
import config_lib

# key | code | date | open | close | high | low | volum

class PriceMeans:

   def __init__(self):
      conf = config_lib.CaBeConfig()
      price_means_out_path = '%s/priceMeans.dat' % conf.get_outpath()
      self.fp = open(price_means_out_path, 'w')
      print '__init__ PriceMeans'

   def __del__(self):
      print '__del__ PriceMeans'
      self.fp.close()
   
   def find(self, lastDate, dataAll):
      print 'Start PriceMeans...'
      for key, lists in dataAll.items():

         #print 'code [%s]' % key
         n5 = 0
         n20 = 0
         n60 = 0
         nbong = 0
         nClose = 0
         nMeans5 = 0
         nMeans20 = 0
         nMeans60 = 0
         n4total = 0
         n19total = 0
         n59total = 0
         lastWorkDayStartV = 0
         lastWorkDayEndV = 0
         total_bong = len(lists)


         for items in lists:
            fields = items.split('|')
            if nbong == 0:
               lastWorkDayOpen    = int(fields[3])
               lastWorkDayClose   = int(fields[4])
               #print 'code [%s], date[%s], Open[%d], Close[%d]' % (fields[1], fields[2], lastWorkDayOpen, lastWorkDayClose)

            nbong += 1
            nClose = int(fields[4])

            # 5 means
            if nbong <= 5 and total_bong >= 5:
               n5 += nClose
               if nbong == 5:
                  nMeans5 = n5 / 5

               if nbong != 1:
                  n4total += nClose

            # 20 means
            if nbong <= 20 and total_bong >= 20:
               n20 += nClose
               if nbong == 20:
                  nMeans20 = n20 / 20

               if nbong != 1:
                  n19total += nClose
                  
            # 60 means
            if nbong <= 60 and total_bong >= 60:
               n60 += nClose
               if nbong == 60:
                  nMeans60 = n60 / 60

               if nbong != 1:
                  n59total += nClose
          

            fields = items.split('|')
            if nbong > 60:
               break


         buf = '%s|%d|%d|%d|%d|%d|%d\n' % (key, nMeans5, n4total, nMeans20, n19total, nMeans60, n59total)
         self.fp.write(buf)
         #print 'code[%s], 5[%d] 5b[%d] 20[%d] 20b[%d] 60[%d] 60b[%d]' % (key, nMeans5, n4total, nMeans20, n19total, nMeans60, n59total)

# end

