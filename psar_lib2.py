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

      self.highval = 0
      self.lowval = 0
      self.direction = 0
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
      self.nHigh = h

   def getHigh(self):
      return self.nHigh

   def setLow(self, l):
      self.nLow = l

   def getLow(self):
      return self.nLow

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

      if self.ep != 0:
         print 'step 1'
         if self.direction == 1:
            self.ep = self.highval
            self.sar1 = self.sar1 + self.afval * (self.ep - self.sar1)
            if self.nHigh > self.highval:
               self.highval = self.nHigh
               self.afval = self.afval + self.Af
               if self.afval >= self.MaxAf:
                  self.afval = self.MaxAf

            if self.nLow < self.sar1:
               self.direction = -1
               self.sar1 = self.ep
               self.afval = 0
               self.ep = 0
               self.lowval = self.nLow
         else:
            self.ep = self.lowval
            self.sar1 = self.sar1 + self.afval * (self.ep - self.sar1)
            if self.nLow < self.lowval:
               self.lowval = self.nLow
               self.afval = self.afval + self.Af
               if self.afval >= self.MaxAf:
                  self.afval = self.MaxAf
            elif self.nHigh > self.sar1:
               self.direction = 1
               self.sar1 = self.ep
               self.afval = 0
               self.ep = 0
               self.highval = self.nHigh
      elif self.sar1 != 0 and self.ep == 0:
         print 'step 2'
         if self.direction == 1:
            self.ep = self.highval
            self.afval = self.Af
            self.sar1 = self.sar1 + self.afval * (self.ep - self.sar1)
            if self.nHigh > self.highval:
               self.highval = self.nHigh
               self.afval = self.afval + self.Af
               if self.afval >= self.MaxAf:
                  self.afval = self.MaxAf
            else:
               self.ep = self.lowval
               self.afval = self.Af
               self.sar1 = self.sar1 + self.afval * (self.ep - self.sar1)
               if self.nLow < self.lowval:
                  self.lowval = self.nLow
                  self.afval = self.afval + self.Af
                  if self.afval >= self.MaxAf:
                     self.afval = self.MaxAf
      else:
         print 'step 3'
         if self.direction == 0:
            if todayC > yesterdayC:
               self.direction = 1
            elif todayC < yesterdayC:
               self.direction = -1
         elif self.direction == 1:
            if todayC < yesterdayC:
               self.direction = -1
               self.sar1 = self.highval
         elif self.direction == -1:
            if todayC > yesterdayC:
               self.direction = 1
               self.sar1 = self.lowval

         self.lowval  = min(self.nLow, self.lowval)
         self.highval = max(self.nHigh, self.highval)

      #if self.sar1 != 0:
         #print 'sar1 : [%s]' % str(self.sar1)
         #User_Func_Sar = sar1
   

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
