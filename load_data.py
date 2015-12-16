# -*- coding: UTF-8 -*-

import urllib.request
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

try:
	

	if len(sys.argv) < 2:
		print ('please input card_set %d', len(sys.argv))
		logging.error('please input card_set')
		raise

	if sys.argv[1] not in card_set:
		print('please input right card_set')
		logging.error('please input right card_set')
		raise

	set = sys.argv[1]

	for language in language_set:

		if os.path.exists('card_data') == False:

			os.mkdir('card_data')

		if os.path.exists("card_data/%s"%(set)) == False:

			os.mkdir("card_data/%s"%(set))

		if os.path.exists("card_data/%s/%s"%(set, language)) == False:

			os.mkdir("card_data/%s/%s"%(set, language))

		if os.path.exists("card_data/%s/%s/images"%(set, language)) == False:

			os.mkdir("card_data/%s/%s/images"%(set, language))


		if os.path.exists("card_data/%s/%s/%s_%s.html"%(set, language, set, language)) == False:

			urllib.request.urlretrieve("http://magiccards.info/%s/%s.html"%(set, language), "card_data/%s/%s/%s_%s.html"%(set, language, set, language))
			print ('http://magiccards.info/%s/%s.html'%(set, language))
			logging.info('http://magiccards.info/%s/%s.html'%(set, language))

		f = codecs.open("card_data/%s/%s/%s_%s.html"%(set, language, set, language), 'r', 'utf8')

		content = f.read()

		soup = BeautifulSoup(content, 'html.parser')

		f.close()

		card_num = []
		for link in soup.select('a'):
			
			if "/%s/%s/"%(set, language) in link.get('href'):
				m = re.search('\d+[a-z]?', link.get('href'))
				card_num.append(m.group(0))

		for number in card_num:
			if os.path.exists("card_data/%s/%s/%s.html"%(set, language, number)) == False:
				urllib.request.urlretrieve("http://magiccards.info/%s/%s/%s.html"%(set, language, number), "card_data/%s/%s/%s.html"%(set, language, number))
				print ("http://magiccards.info/%s/%s/%s.html"%(set, language, number))
				logging.info("http://magiccards.info/%s/%s/%s.html"%(set, language, number))
				time.sleep(10)

			if os.path.exists("card_data/%s/%s/images/%s.jpg"%(set, language, number)) == False:
				urllib.request.urlretrieve("http://magiccards.info/scans/%s/%s/%s.jpg"%(language, set, number), "card_data/%s/%s/images/%s.jpg"%(set, language, number))
				print ("http://magiccards.info/scans/%s/%s/%s.jpg"%(language, set, number))
				logging.info("http://magiccards.info/scans/%s/%s/%s.jpg"%(language, set, number))
				time.sleep(10)

except:
	print("Unexpected error:", sys.exc_info()[0])
	logging.error("Unexpected error:", sys.exc_info()[0])