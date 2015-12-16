# -*- coding: UTF-8 -*-

import codecs
import os
import logging
import sys
import time
import re
from bs4 import BeautifulSoup

logging.getLogger( __name__ )
logging.basicConfig(level=logging.DEBUG,
	                format='[%(levelname)s] [%(asctime)s] [%(filename)s] [line:%(lineno)d] [%(message)s]',
	                datefmt='%a, %d %b %Y %H:%M:%S',
	                filename='log.txt',
	                filemode='a')

exec(open(os.getcwd() + "/config/config.py").read())

#f = codecs.open("card_data/%s/%s/%s_%s.html"%(set, language, set, language), 'r', 'utf8')
f = codecs.open("card_data/bfz/en/1.html", 'r', 'utf8')

content = f.read()

soup = BeautifulSoup(content, 'html.parser')

f.close()

cardinfo = {}

cardinfo[0]  = {}

cardinfo[0]['card_name'] = soup.select('span a')[0].text.strip()

print(soup.select('table p')[0].text)

content = soup.select('table p')[0].text

a = content.split()

print(soup.select('span a'))