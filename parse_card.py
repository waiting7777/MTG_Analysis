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
f = codecs.open("card_data/bfz/en/bfz_en.html", 'r', 'utf8')

content = f.read()

soup = BeautifulSoup(content, 'html.parser')

f.close()

w = codecs.open('test.txt', 'w', 'utf8')

cardinfo = {}
flag = 0

print(soup.select('table[cellpadding="3"] tr td'))

for item in soup.select('table[cellpadding="3"] tr'):
	if flag == 0:
		flag += 1
		continue
	
	temp = item.text.split('\n')

	for i in range(1, 7):
		w.write(temp[i] + ', ')
	w.write('\n')


