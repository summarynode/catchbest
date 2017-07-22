#!/usr/bin/python
# coding=utf8

import sys
import pymysql
import redis
import time
import config_lib

# key | code | date | open | close | high | low | volum

class PSar:

   def __init__(self):
      conf = config_lib.CaBeConfig()
      file_path = '%s/psar.dat' % conf.get_outpath() 
      self.fpOut = open(file_path, 'w')
      print '__init__ PSar'


   def __del__(self):
      self.fpOut.close()
      print '__del__ PSar'


   def find(self, maxBong, dataAll):

      for key, value in dataAll.items():

         nBong = 0
         item_total = 0
         length = len(value)
         dates  = [None] * length
         highs  = [None] * length
         lows   = [None] * length
         closes = [None] * length
         psar   = [None] * length
         psarbull = [None] * length
         psarbear = [None] * length
         bull = True
         iaf = 0.02
         maxaf = 0.2
         af = iaf

         value.reverse()

         for items in value:
            fields = items.split('|')
            dates[item_total]  = str(fields[2])
            highs[item_total]  = int(fields[5])
            lows[item_total]   = int(fields[6])
            closes[item_total] = int(fields[4])
            psar[item_total]   = int(fields[4])
            item_total += 1


         hp = highs[0]
         lp = lows[0]
            
         for items in value:
            fields  = items.split('|')
            sdate   = str(fields[2])
            nOpen   = int(fields[3])
            nClose  = int(fields[4])
            nHigh   = int(fields[5])
            nLow    = int(fields[6])
            scode   = str(fields[1])
            volum   = str(fields[7])

            if nBong == 0 or nBong == 1:
               nBong += 1
               continue

            if bull:
               psar[nBong] = psar[nBong - 1] + af * (hp - psar[nBong - 1])
            else:
               psar[nBong] = psar[nBong - 1] + af * (lp - psar[nBong - 1])

            reverse = False

            if bull:
               if lows[nBong] < psar[nBong]:
                  bull = False
                  reverse = True
                  psar[nBong] = hp
                  lp = lows[nBong]
                  af = iaf
            else:
               if highs[nBong] > psar[nBong]:
                  bull = True
                  reverse = True
                  psar[nBong] = lp
                  hp = highs[nBong]
                  af = iaf


            if not reverse:
               if bull:
                  if highs[nBong] > hp:
                     hp = highs[nBong]
                     af = min(af + iaf, maxaf)
                  if lows[nBong - 1] < psar[nBong]:
                     psar[nBong] = lows[nBong - 1]
                  if lows[nBong - 2] < psar[nBong]:
                     psar[nBong] = lows[nBong - 2]
               else:
                  if lows[nBong] < lp:
                     lp = lows[nBong]
                     af = min(af + iaf, maxaf)
                  if highs[nBong - 1] > psar[nBong]:
                     psar[nBong] = highs[nBong - 1]
                  if highs[nBong - 2] > psar[nBong]:
                     psar[nBong] = highs[nBong - 2]

               if bull:
                  psarbull[nBong] = psar[nBong]
                  if sdate == "20170629":
                     print 'bull [%s] [%s]' % (scode, sdate)
               else:
                  psarbear[nBong] = psar[nBong]
                  if sdate == "20170629":
                     print 'bear [%s] [%s]' % (scode, sdate)

            nBong += 1


         # scode | bull | hp | lp | af | psar[nbong-1]
         buf = '%s|%s|%f|%f|%f|%f\n' % (scode, str(bull), hp, lp, af, psar[nBong - 2])
         self.fpOut.write(buf)



   if __name__ == "__main__":
      print 'start - end'
          

#end 
