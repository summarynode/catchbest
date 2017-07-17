#!/usr/bin/python
# -*- coding: cp949 -*-

import sys
import pymysql
import redis
import time
import config_lib


dataAll = {}


def prints(x):
   print x


def loadingAllDayData(curs):
   sql = "select s_code, s_date, s_open, s_close, s_high, s_low, s_amount from day_main"
   curs.execute(sql)
   rows = curs.fetchall()
  
   total = 0
   key = ''
   for row in rows:
      total += 1
      #print '[%d] code : %s, date : %s, open : %d, close : %d, high : %d, low : %d, amount : %d' % (total, row[0], row[1], row[2], row[3], row[4], row[5], row[6])
      key = row[0] + '-' + row[1]
      dataAll[key] = 0
      #print key

   print 'Loading end !'
      

def isExistData(x):
   if x in dataAll:
      return True
   else:
      return False


def connectMysql():
   #conn = pymysql.connect(host='erpyjun2.cafe24.com', user='erpy', password='kiwitomato.com', db='day_data', charset='utf8')
   conn = pymysql.connect(host='localhost', user='erpy', password='kiwitomato.com', db='day_data', charset='utf8')
   curs = conn.cursor()
   return conn, curs


def closeMysql(conn):
   conn.commit()
   conn.close()

def argCheck():
   if len(sys.argv) != 2:
      print '(USAGE) filepath table_name'
      return False
   
   return True


def connectRedis():
   redi = redis.StrictRedis(host='localhost', port=7379, db=0)
   return redi


def isExistRedis(key, redi):
   if len(key.strip()) == 0:
      return False

   r_value = redi.get(key)
   if r_value == None:
      return False

   if len(r_value.strip()) == 0:
      return False

   return True
   

if __name__ == "__main__":

   if argCheck() != True:
      sys.exit()

   print 'argv[0] : %s' % sys.argv[0]
   print 'argv[1] : %s' % sys.argv[1]

   total = 0
   ldate = long(sys.argv[1])
   p_start = time.time()

   r = connectRedis()

   conf = config_lib.CaBeConfig()
   file_path = "%s/1bong-price-%s.log" % (conf.get_outpath(), sys.argv[1])
   f = open(file_path, 'w')

   for rkey in r.scan_iter():
      total += 1
      r_value = str(r.get(rkey)).strip()

      fields = r_value.split('|')
      if len(fields) != 7:
         print 'fields length is NOT 7'
         continue
      
      lCurDate = long(fields[1])
      if lCurDate >= ldate:
         #print 'SKIP [%d]' % lCurDate
         continue

      buf = '%s|%s\n' % (rkey, r_value)
      f.write(buf)
      
      #print '%s:%s' % (rkey, r_value)
      if total % 10000 == 0:
         print 'proc [%d] [%s]' % (total, rkey)


   f.close()

   p_done = time.time() 
   p_elapsed = p_done - p_start
   print 'End. total [%d] [%s]' % (total, str(p_elapsed))
