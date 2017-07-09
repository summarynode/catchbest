#!/usr/bin/python
# -*- coding: cp949 -*-

import sys
import pymysql
import redis
import time
import ConfigParser


class CaBeConfig:

   def __init__(self):
      conf_file = '/home/erpy/catchbest/catchbest.conf'
      self.config = ConfigParser.ConfigParser()
      self.config.read(conf_file)
      self.out_path = self.config.get('path','out_path')
      self.raw_path = self.config.get('path','raw_path')
      print 'out_path [%s]' % (self.out_path)
      print 'raw_path [%s]' % (self.raw_path)
      print '__init__'

   def get_outpath(self):
      return self.out_path

   def get_rawpath(self):
      return self.raw_path

