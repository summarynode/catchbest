#!/usr/bin/python
# coding=utf8

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
import day_price_lib
import day_gapsang_umbong_lib
import config_lib

if __name__ == "__main__":

   if len(sys.argv) != 2:
      print 'USAGE: key'
      sys.exit()

   key = str(sys.argv[1])
   print 'key : %s' % str(sys.argv[1])
   
   conf = config_lib.CaBeConfig()
   
   # init class
   day = day_lib.DayService()
   r = day.connectRedis()
   allOut = str(day.getRedis(key, r)).replace("[","").replace("]","").replace("'","")
   
   print 'allOut [%s]' % allOut

   alist = allOut.split(",")
   for items in alist:
      fields = items.split("|")
      if len(fields) == 2:
         print 'list : %s, %s' % (fields[0], fields[1])

   """
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

   day_price = day_price_lib.DayPrice()
   day_price.find(sdate, dataAll)

   day_gapsang_umbong = day_gapsang_umbong_lib.GapSangUm()
   day_gapsang_umbong.find(sdate, dataAll)
   """


   """
   for key, value in dataAll.items():
      for items in value:
         print '[%s] [%s]' % (key, items)
   """

   
   print 'end'

