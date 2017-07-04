#!/usr/bin/python
# -*- coding: cp949 -*-

import bun_lib

if __name__ == "__main__":
   bun = bun_lib.BunService()
   bun.cprint(99)

   dataAll = bun.loading('20170703')

   for key, value in dataAll.items():
      for items in value:
         print '[%s] [%s]' % (key, items)
   
   print 'end'

