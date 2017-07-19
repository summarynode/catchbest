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

   if len(sys.argv) != 3:
      print 'USAGE: [key] [value]'
      sys.exit()

   key = str(sys.argv[1])
   r_value = str(sys.argv[2])
   print 'key [%s], value[%s]' % (key, r_value)
   
   day = day_lib.DayService()
   r = day.connectRedis()
   day.setRedis(key, r_value, r)
   
   print 'end'

