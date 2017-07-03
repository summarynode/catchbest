#!/usr/bin/python
# -*- coding: cp949 -*-

import sys
import pymysql
import redis
import time


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
   exist_count = 0
   insert_count = 0
   insert_err_count = 0
   p_start = time.time()

   r = connectRedis()
   f = open(sys.argv[1], 'r')


   while True:
      line = f.readline()
      if not line: break
      #sys.stdout.write(line)

      line_arr = line.split("|")
      list_size = len(line_arr)
      #print 'line_arr size : %d' % (len(line_arr))

      if list_size != 7:
         continue
        
         """
         print '0) %s' % (line_arr[0])   # code
         print '1) %s' % (line_arr[1])   # date
         print '2) %s' % (line_arr[2])   # open
         print '3) %s' % (line_arr[3])   # end
         print '4) %s' % (line_arr[4])   # high
         print '5) %s' % (line_arr[5])   # low
         print '6) %s' % (line_arr[6])   # value 
         """

      total += 1

      if total % 10000 == 1:
         print 't[%d] i[%d] e[%d]' %(total, insert_count, exist_count)

      key = line_arr[0] + '-' + line_arr[1]
      if isExistRedis(key, r) == True:
         #print 'exist [%s]' % key
         exist_count += 1
         continue

      ret = r.set(key, line)
      if ret == False:
         insert_err_count += 1
         #print 'False redis set : [%s]' % key
      else:
         insert_count += 1
         #print 'set key [%s]' % (key)

   p_done = time.time()

   f.close()
   print 'End total[%d] skip[%d] insert[%d] elapse[%s]' % (total, exist_count, insert_count, str(p_done - p_start))

