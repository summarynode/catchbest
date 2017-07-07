#!/usr/bin/python
# -*- coding: cp949 -*-

import day_lib
import day_high_value_lib
import day_close_price_lib
import day_price_means_lib
import day_bollben_lib

if __name__ == "__main__":
   # init class
   day = day_lib.DayService()
   dataAll = day.loading('20170630')

   day_find_high = day_high_value_lib.HighValue()
   #day_find_high.find(200, dataAll)

   day_close_price = day_close_price_lib.ClosePrice()
   #day_close_price.find(dataAll, '20170610')

   day_price_means = day_price_means_lib.PriceMeans()
   day_price_means.find('20170707', dataAll)

   day_bollen = day_bollben_lib.BollBen()
   day_bollen.find('20170707', dataAll)


   """
   for key, value in dataAll.items():
      for items in value:
         print '[%s] [%s]' % (key, items)
   """
   
   print 'end'

