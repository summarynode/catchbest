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

      self.High = 0
      self.Low = 0
      self.Close = 0
      self.Date = ""
      self.highval = 0
      self.lowval = 0
      self.direction = True # bull
      self.sar1 = 0
      self.afval = 0
      self.ep = 0
      self.count = 0
      self.MaxAf = 0.2
      self.Af = 0.02

      conf = config_lib.CaBeConfig()
      file_path = '%s/psar.dat' % conf.get_outpath() 
      self.fpOut = open(file_path, 'w')
      print '__init__ PSar'


   def __del__(self):
      self.fpOut.close()
      print '__del__ PSar'

   def setHigh(self, h):
      self.High = h

   def getHigh(self):
      return self.High

   def setLow(self, l):
      self.Low = l

   def getLow(self):
      return self.Low

   def setClose(self, c):
      self.Close = c

   def getClose(self):
      return self.Close

   def setDate(self, d):
      self.Date = d

   def getDate(self):
      return self.Date

   def addCount(self):
      self.count = self.count + 1

   def initCount(self):
      self.count = 0

   def getSar(self):
      return self.sar1

   def psar(self, todayC, yesterdayC):

      if self.count == 0:
         self.highval = self.nHigh
         self.lowval  = self.nLow
         self.direction = 0
         self.sar1 = 0
         self.afval = 0
         self.ep = 0
         self.MaxAf = 0.2
         self.Af = 0.02


   def find(self, maxBong, dataAll):
      for key, value in dataAll.items():

         #print 'code [%s]' % key
         nBong = 0
         self.initCount()

         for items in reversed(value):
            fields = items.split('|')
            sdate   = int(fields[2])
            nOpen   = int(fields[3])
            nClose  = int(fields[4])
            nHigh   = int(fields[5])
            nLow    = int(fields[6])
            scode   = str(fields[1])
            volum   = str(fields[7])

            if nBong == 0:
               self.setLow(nLow)
               self.setHigh(nHigh)

            if nBong > 0:
               todayC = nClose
               self.psar(todayC, yesterdayC)
               self.addCount()
               print 'psar [%s] [%s] [%s] high[%d] low[%d] todayC[%d] yesC[%d]' % (scode, str(self.getSar()), sdate, nHigh, nLow, todayC, yesterdayC)

            yesterdayC = nClose

            if self.getLow() > nLow:
               self.setLow(nLow)
            
            if self.getHigh() < nHigh:
               self.setHigh(nHigh)

            nBong += 1 

         #buf = '%s|%d|%d|%d|%d|%s\n' % (scode, nOpen, nClose, nHigh, nLow, volum)
         #self.fpOut.write(buf)
         #print '[para] [%s] [%s]' % (scode, buf.strip())


   if __name__ == "__main__":
      print 'start - end'
          

#end 
