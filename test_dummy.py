#!/usr/bin/python
# coding=utf8

import sys
import day_lib
import config_lib
import day_acc_volum_lib

if __name__ == "__main__":

   if len(sys.argv) != 2:
      print 'USAGE: date'
      sys.exit()

   sdate = str(sys.argv[1])
   if len(sdate) != 8:
      print 'date is not 8 length!!'
      sys.exit()

   acc = day_acc_volum_lib.AccVolume()
   dataAll = acc.loading(sdate)
   acc.find(dataAll)
   
   print 'end'

#end
