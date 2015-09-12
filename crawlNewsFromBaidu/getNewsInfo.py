# -*- coding:utf-8 -*-
__author__ = 'yueg'
import scrapy
import re
from crawlNewsFromBaidu import editDistance
from bs4 import BeautifulSoup as bsp
import HTMLParser
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class newsInfo():
    pass
