#!/usr/bin/python
# coding=utf8

import os
import sys
import day_lib
import config_lib
import day_acc_volum_lib
import day_acc_volum_db_lib

if __name__ == "__main__":

   if len(sys.argv) != 2:
      print 'USAGE: date'
      sys.exit()

   sdate = str(sys.argv[1])
   if len(sdate) != 8:
      print 'date is not 8 length!!'
      sys.exit()

   raw_path = '/home/erpy/raw_data'
   for dirName, subdirList, fileList in os.walk(raw_path):
      print('Found directory: [%s]' % dirName)
      for fname in fileList:
         s = fname
         sdate = s[6:14]
         print'file [%s][%s]' % (fname, sdate)

         acc = day_acc_volum_lib.AccVolume()
         dataAll = acc.loading(sdate)
         acc.find(dataAll)
         dataAll = []

         accdb = day_acc_volum_db_lib.AccVolumeDB()
         accdb.insertAll(sdate)
   
   print 'end'

#end
