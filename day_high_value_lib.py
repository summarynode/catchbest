#!/usr/bin/python
# -*- coding: cp949 -*-

import sys
import pymysql
import redis
import time

class HighValue:

   def __init__(self):
      print 'init HighValue'
   
   def find(self, nbong, dataAll):
      for key, value in dataAll.items():
         print 'code [%s]' % key
         for items in value:
            fields = items.split('|')
            print 'code [%s], date[%s]' % (fields[1], fields[2])
            #print '[%s] [%s]' % (key, items)
          

