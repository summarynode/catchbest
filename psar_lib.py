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
      self.MaxAf = 0

      conf = config_lib.CaBeConfig()
      file_path = '%s/psar.dat' % conf.get_outpath() 
      self.fpOut = open(file_path, 'w')
      print '__init__ PSar'


   def __del__(self):
      self.fpOut.close()
      print '__del__ PSar'


   def psar(self):
      if count == 0:
         self.highval = nHigh
         self.lowval  = nLow
         self.direction = 0
         self.sar1 = 0
         self.afval = 0
         self.ep = 0
         self.count = 1

      if self.ep != 0:
         if self.direction == 1:
            self.ep = self.highval
            self.sar1 = self.sar1 + self.afval * (self.ep - self.sar1)
            if nHigh > self.highval:
               self.highval = nHigh
               self.afval = self.afval + Af
               if self.afval >= self.MaxAf:
                  self.afval = self.MaxAf

            if nLow < self.sar1:
               self.direction = -1
               self.sar1 = self.ep
               self.afval = 0
               self.ep = 0
               self.lowval = nLow
         else:
            self.ep = self.lowval
            self.sar1 = self.sar1 + self.afval * (self.ep - self.sar1)
            if nLow < self.lowval:
               self.lowval = nLow
               self.afval = self.afval + Af
               if self.afval >= self.MaxAf:
                  self.afval = self.MaxAf
            elif nHigh > self.sar1:
               self.direction = 1
               self.sar1 = self.ep
               self.afval = 0
               self.ep = 0
               self.highval = nHigh
      elif self.sar1 != 0 and self.ep == 0:
         if self.direction == 1:
            self.ep = self.highval
            self.afval = Af
            self.sar1 = self.sar1 + self.afval * (self.ep - self.sar1)
            if nHigh > self.highval:
               self.highval = nHigh
               self.afval = self.afval + Af
               if self.afval >= self.MaxAf:
                  self.afval = self.MaxAf
            else:
               self.ep = self.lowval
               self.afval = Af
               self.sar1 = self.sar1 + self.afval * (self.ep - self.sar1)
               if nLow < self.lowval:
                  self.lowval = nLow
                  self.afval = self.afval + Af
                  if self.afval >= self.MaxAf:
                     self.afval = self.MaxAf
      else:
         if self.direction == 0:
            if c > c[1]:
               self.direction = 1
            elif c < c[1]:
               self.direction = -1
         elif self.direction == 1:
            if c < c[1]:
               self.direction = -1
               self.sar1 = self.highval
         elif self.direction == -1:
            if c > c[1]:
               self.direction = 1
               self.sar1 = self.lowval

         self.lowval  = min(nLow, self.lowval)
         self.highval = max(nHigh, self.highval)

      if self.sar1 != 0:
         print 'sar1 : [%s]' % str(sar1)
         #User_Func_Sar = sar1
   

   def find(self, maxBong, dataAll):
      for key, value in dataAll.items():

         #print 'code [%s]' % key
         nBong = 0

         for items in value:
            fields = items.split('|')
            nOpen   = int(fields[3])
            nClose  = int(fields[4])
            nHigh   = int(fields[5])
            nLow    = int(fields[6])
            scode   = str(fields[1])
            volum   = str(fields[7])

            nBong += 1 

         buf = '%s|%d|%d|%d|%d|%s\n' % (scode, nOpen, nClose, nHigh, nLow, volum)
         self.fpOut.write(buf)
         print '[DayPrice] [%s] [%s]' % (scode, buf.strip())


   if __name__ == "__main__":
      print 'start - end'
          

#end 
