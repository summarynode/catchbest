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

         self.sixPriceMeansDic[skey] = float(fields[1].strip())
         print 'skey [%s] [%s]' % (skey, str(fields))

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
                     priceMeans = float(fields[4])

                  #lnTmp = pow(2, (int(fields[4]) - priceMeans))
                  lnTmp = (float(fields[4]) - priceMeans) ** 2
                  n20 += lnTmp

                  if nBong == 20:
                     siTmp = n20 / 19.0
                     # bollBen LOW
                     bollBenLow = priceMeans - (math.sqrt(siTmp) * 2)
                     # bollBen TOP
                     bollBenTop = priceMeans + (math.sqrt(siTmp) * 2)
                     
                     print '[볼벤하단] [%s] [%s] 하단[%f] 상단[%f]' % (fields[1], curDate, bollBenLow, bollBenTop)

                     if self.isSurpassBollbenLowLine(lastWorkDayHigh, lastWorkDayLow, bollBenLow):
                        print '[bollBen low line surpass] [%s] [%s]' % (fields[1], curDate)
                     else:
                        # lowPrice vs bollBenLowLine
                        siPer = ((bollBenLow / lastWorkDayLow) -1) * 100
                        if abs(siPer) < 1.5:
                           print '[lowPrice bollBen low line touch] [%s] [%s] [%f]' % (fields[1], curDate, abs(siPer))

                        # highPrice vs bollBenLowLine
                        siPer = ((bollBenLow / lastWorkDayHigh) -1) * 100
                        if abs(siPer) < 1.5:
                           print '[highPrice bollBen low line touch] [%s] [%s] [%f]' % (fields[1], curDate, abs(siPer))



# end

