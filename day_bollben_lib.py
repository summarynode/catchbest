#!/usr/bin/python
# coding=utf8

import sys
import pymysql
import redis
import time
import config_lib
import math

# key | code | date | open | close | high | low | volum

class BollBen:

   def __init__(self):
      self.sixPriceMeansDic = {}
      self.bollBenTouchDic = {}
      conf = config_lib.CaBeConfig()

      six_price_means_path = '%s/5priceMeans.dat' % conf.get_outpath()
      self.fpPriceMeans = open(six_price_means_path, 'r')

      bollben_out_path = '%s/bollBen.dat' % conf.get_outpath()
      self.fpBollBen = open(bollben_out_path, 'w')

      while True:
         line = self.fpPriceMeans.readline().strip()
         if not line:
            print 'priceMeans breaking...'
            break

         fields = line.split('|')
         if len(fields) != 2:
            print 'skip is not 2 items [%s]' % (line)
            continue

         skey = str(fields[0])

         self.sixPriceMeansDic[skey] = round(float(fields[1].strip()), 2)
         print '[5 Days PM Loading key] [%s] [%f]' % (skey, self.sixPriceMeansDic[skey])

      self.fpPriceMeans.close()
      print 'init BollBen'


   def __del__(self):
      self.fpPriceMeans.close()
      self.fpBollBen.close()
      print '__del__ BollBen'

   
   def isSurpassBollbenLowLine(self, topPrice, lowPrice, bollbenLow):
      if topPrice >= bollbenLow and lowPrice <= bollbenLow:
         return True
      return False


   def isBollbenList(self, scode):
      if scode in self.bollBenTouchDic:
         return True
      return False


   def find(self, lastDate, dataAll):
      print 'Start BollBen...'
      for key, lists in dataAll.items():

         for nIndex in range(0,6):

            n20 = 0.0
            lnTmp = 0.0
            siTmp = 0.0
            siPer = 0.0
            bollBenLow = 0.0
            bollBenTop = 0.0
            nBong = 0
            nOpen = 0
            nClose = 0
            siLastPer = 0.0
            skip_count = 0
            priceMeans = 0.0
            lastWorkDayOpen = 0
            lastWorkDayClose = 0
            lastWorkDayHigh = 0
            lastWorkDayLow = 0
            totalBong = len(lists)

            for items in lists:

               if skip_count < nIndex:
                  skip_count += 1
                  continue

               fields = items.split('|')

               if nBong == 0 and nIndex == 0:
                  nOpen  = int(fields[3])
                  nClose = int(fields[4])
                  if nOpen < nClose:
                     siLastPer = ((nClose / nOpen) - 1) * 100
                  else:
                     siLastPer = 0.0

               if nBong == 0:
                  lastWorkDayOpen  = int(fields[3])
                  lastWorkDayClose = int(fields[4])
                  lastWorkDayHigh  = int(fields[5])
                  lastWorkDayLow   = int(fields[6])
                  curDate          = str(fields[2])
                  #print 'code [%s], date[%s], Open[%d], Close[%d]' % (fields[1], fields[2], lastWorkDayOpen, lastWorkDayClose)
                   
               nBong += 1

               if nBong <= 20 and totalBong >= 20:
                  skey = '%s_%s' % (fields[1], fields[2])
                  if skey in self.sixPriceMeansDic:
                     priceMeans = self.sixPriceMeansDic[skey]
                  else:
                     print 'Breaking nBong[%d]' % nBong
                     break

                  #lnTmp = pow(2, (int(fields[4]) - priceMeans))
                  lnTmp = round((float(fields[4]) - priceMeans) ** 2, 2)
                  n20 += lnTmp

                  if nBong == 20:
                     siTmp = n20 / 20.0
                     # bollBen LOW
                     bollBenLow = round(priceMeans - (math.sqrt(siTmp) * 2), 2)
                     # bollBen TOP
                     bollBenTop = round(priceMeans + (math.sqrt(siTmp) * 2), 2)
                     
                     print '[BollBen] [%s] [%s] LOW[%f] TOP[%f]' % (fields[1], curDate, bollBenLow, bollBenTop)

                     if self.isSurpassBollbenLowLine(lastWorkDayHigh, lastWorkDayLow, bollBenLow):
                        if self.isBollbenList(fields[1]) == False:
                           buf = '%s|SU|%f|%d|%d\n' % (fields[1], bollBenLow, lastWorkDayLow, lastWorkDayHigh)
                           self.fpBollBen.write(buf)
                           self.bollBenTouchDic[fields[1]] = "SU"
                           print '[bollBen low line surpass] [%s] [%s]' % (fields[1], curDate)
                     else:
                        # lowPrice vs bollBenLowLine
                        siPer = ((bollBenLow / lastWorkDayLow) -1) * 100
                        if abs(siPer) < 1.5:
                           if self.isBollbenList(fields[1]) == False:
                              buf = '%s|LO|%f|%f\n' % (fields[1], bollBenLow, abs(siPer))
                              self.fpBollBen.write(buf)
                              self.bollBenTouchDic[fields[1]] = "LO"
                              print '[lowPrice bollBen LOW line touch] [%s] [%s] [%f]' % (fields[1], curDate, abs(siPer))

                        # highPrice vs bollBenLowLine
                        siPer = ((bollBenLow / lastWorkDayHigh) -1) * 100
                        if abs(siPer) < 1.5:
                           if self.isBollbenList(fields[1]) == False:
                              buf = '%s|TO|%f|%f\n' % (fields[1], bollBenLow, abs(siPer))
                              self.fpBollBen.write(buf)
                              self.bollBenTouchDic[fields[1]] = "TO"
                              print '[highPrice bollBen TOP line touch] [%s] [%s] [%f]' % (fields[1], curDate, abs(siPer))

# end
