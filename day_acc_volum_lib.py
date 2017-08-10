#!/usr/bin/python
# coding=utf8

import sys
import os
import time
import operator

import pymysql
import redis
import day_lib
import config_lib

"""
code^
+-sign^
accVolum^
+-close^
+-Open^
+-High^
+-Low^
signTime^
signPower^
+-PricePer^
sellRemain^
buyRemain
"""

class AccVolume:

   def __init__(self):
      self.sdate = ""
      self.allData = []
      conf = config_lib.CaBeConfig()
      self.day = day_lib.DayService()

      out_path = '%s/accVolume.dat' % conf.get_outpath()
      self.fpOut = open(out_path, "w")

      print '__init__ AccVolume'

   def __del__(self):
      self.fpOut.close()
      print '__del__ AccVolume'
   

   def loading(self, sdate):
      self.sdate = sdate
      conf = config_lib.CaBeConfig()
      dummy_path = '%s/dummy-%s.log' % (conf.get_rawpath(), sdate)
      fpDummy = open(dummy_path, 'r')
      full_size = os.fstat(fpDummy.fileno()).st_size

      total_line = 0
      skip_line = 0

      while True:
         line = fpDummy.readline()
         
         cur_pos = fpDummy.tell()
         if cur_pos >= full_size:
            break

         if len(line.strip()) == 0:
            skip_line += 1
            continue
         
         """
         if not line:
            break
         """

         total_line += 1

         self.allData.append(line.strip())
         #print line

      print 'total line : t[%d] s[%d] size[%d]' % (total_line, skip_line, len(self.allData))

      return self.allData


   def find(self, dataAll):

      k = 0.0
      t = 0.0
      signAll = {}
      volAll  = {}
      resultAll = {}

      # calculate acc_volume
      for items in dataAll:
         fields = items.split('^')
         if len(fields) != 13:
            print 'Error fiedls len not 13 : [%d]' % (len(fields))
            continue

         sCode = fields[0]
         nSign = float(fields[1])
         nVolume = float(fields[2])

         # acc sign
         if sCode in signAll:
            k = signAll[sCode]
            t = k + (nSign)
            signAll[sCode] = t
         else:
            signAll[sCode] = nSign

         # volume
         volAll[sCode] = nVolume


      st_total = 0
      sper = 0.0
      per = 0.0

      # calculate acc_volume VS volume
      for key, value in signAll.iteritems():
         st_total += 1
         if signAll[key] < 0:
            continue

         sper = signAll[key] / volAll[key]
         per = sper * 100.0
         resultAll[key] = per

         """
         if per > 25 and signAll[key] > 200000:
            print '[%d] [%s] [%d] [%d] [%f] [%f]' % (st_total, key, value, volAll[key], round(sper,2), round(per,2))
         """

      st_total = 0

      for key, value in resultAll.iteritems():
         st_total += 1
         print '%d) [%s] [%f] [%d] [%d]' % (st_total, key, resultAll[key], signAll[key], volAll[key])
         buf = "%s|%s|%f|%d|%d\n" % (key, self.sdate, resultAll[key], signAll[key], volAll[key])
         self.fpOut.write(buf)

# end
