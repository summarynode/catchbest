#!/usr/bin/python
# -*- coding: cp949 -*-

import sys
import day_lib
import day_high_value_lib
import day_close_price_lib
import day_price_means_lib
import day_bollben_lib
import day_5_price_means_lib
import day_start_point_lib
import day_umumyang_5pms_surpass_lib
import day_singo_lib
import config_lib

if __name__ == "__main__":

   if len(sys.argv) != 2:
      print 'USAGE: date'
      sys.exit()

   sdate = str(sys.argv[1])
   if len(sdate) != 8:
      print 'date is not 8 length!!'
      sys.exit()

   print 'exec name : %s' % str(sys.argv[0])
   print 'date : %s' % str(sys.argv[1])
   
   conf = config_lib.CaBeConfig()
   print 'raw_path [%s]' % conf.get_rawpath()
   print 'out_path [%s]' % conf.get_outpath()
   
   # init class
   day = day_lib.DayService()
   dataAll = day.loading(sdate)

   day_find_high = day_high_value_lib.HighValue()
   day_find_high.find(200, dataAll)

   day_six_price_means = day_5_price_means_lib.SixPriceMeans()
   day_six_price_means.find(sdate, dataAll)

   day_close_price = day_close_price_lib.ClosePrice()
   day_close_price.find(sdate, dataAll)

   day_price_means = day_price_means_lib.PriceMeans()
   day_price_means.find(sdate, dataAll)

   day_bollen = day_bollben_lib.BollBen()
   day_bollen.find(sdate, dataAll)

   day_start_point = day_start_point_lib.StartPoint()
   day_start_point.find(sdate, dataAll)

   day_umumyang_5pms_surpass = day_umumyang_5pms_surpass_lib.Umumyang5Surpass()
   day_umumyang_5pms_surpass.find(sdate, dataAll)

   day_singo = day_singo_lib.Singo()
   day_singo.find(sdate, dataAll)


   """
   for key, value in dataAll.items():
      for items in value:
         print '[%s] [%s]' % (key, items)
   """
   
   print 'end'

