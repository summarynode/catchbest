#!/usr/bin/python
# -*- coding: cp949 -*-

import day_lib
import day_high_value_lib

if __name__ == "__main__":
   # init class
   day = day_lib.DayService()
   day_find_high = day_high_value_lib.HighValue()

   day.cprint(99)
   dataAll = day.loading('20170703')
   day_find_high.find(200, dataAll)

   """
   for key, value in dataAll.items():
      for items in value:
         print '[%s] [%s]' % (key, items)
   """
   
   print 'end'
