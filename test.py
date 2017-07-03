#!/usr/bin/python
# -*- coding: cp949 -*-

import day_lib

if __name__ == "__main__":
   day = day_lib.DayService()
   day.cprint(99)

   dataAll = day.loading('20170703')

   for key, value in dataAll.items():
      for items in value:
         print '[%s] [%s]' % (key, items)
   
   print 'end'

