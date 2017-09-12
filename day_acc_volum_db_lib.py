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
date^
accPer^
signVol^
tradeVol^
"""

class AccVolumeDB:

   def __init__(self):
      self.sdate = ""
      conf = config_lib.CaBeConfig()
      r_path = '%s/accVolume.dat' % conf.get_outpath()
      self.fpRead = open(r_path, "r")

      #self.conn = pymysql.connect(host='erpyjun2.cafe24.com', user='erpy', password='kiwtomato.com', db='day_data', charset='utf8')
      self.conn = pymysql.connect(host='localhost', user='erpy', password='kiwitomato.com', db='day_data', charset='utf8')
      self.curs = self.conn.cursor()


      print '__init__ AccVolumeDB'


   def __del__(self):
      self.fpRead.close()

      self.conn.commit()
      self.curs.close()
      self.conn.close()
      print '__del__ AccVolumeDB'
   

   def insertAll(self, sdate):
      self.sdate = sdate
      full_size = os.fstat(self.fpRead.fileno()).st_size

      sql = ""
      total_insert = 0
      total_error = 0

      while True:
         line = self.fpRead.readline()
         
         cur_pos = self.fpRead.tell()
         if cur_pos >= full_size:
            break

         if len(line.strip()) == 0:
            skip_line += 1
            continue
         
         fields = line.split('|')
         if len(fields) != 5:
            print 'error fields size [%d]' % (len(fields))
            continue

         #sql = "insert into acc_volume (s_code, s_date, s_volume, s_acc_volume, s_per) values ('000111', '20170727', 34334, 434332, 3.10293928)"
         sql = "insert into acc_volume (s_code, s_date, s_volume, s_acc_volume, s_per) values ('%s', '%s', %s, %s, %s)" % (fields[0], fields[1], fields[3], fields[4].strip(), fields[2])

         print sql

         try:
            self.curs.execute(sql)
         except Exception as err:
            print "Exception error [%s]" % str(err)
         
         total_insert += 1

      print 'end t[%d] s[%d]' % (total_insert, total_error)

# end
