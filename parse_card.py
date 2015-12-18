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


def parse_color(card_list, index):

	color_string = ''

	if 'W' in card_list[index]['card_mana']:
		color_string += 'White|'
	if 'U' in card_list[index]['card_mana']:
		color_string += 'Blue|'
	if 'B' in card_list[index]['card_mana']:
		color_string += 'Black|'
	if 'R' in card_list[index]['card_mana']:
		color_string += 'Red|'
	if 'G' in card_list[index]['card_mana']:
   		color_string += 'Green|'
	if 'Artifact' in card_list[index]['card_type']:
		color_string += 'Artifact|'
	if 'Land' in card_list[index]['card_type']:
		color_string += 'Land|'

	return color_string[:-1]


#f = codecs.open("card_data/%s/%s/%s_%s.html"%(set, language, set, language), 'r', 'utf8')
f = codecs.open("card_data/bfz/en/bfz_en.html", 'r', 'utf8')

content = f.read()

soup = BeautifulSoup(content, 'html.parser')

f.close()

w = codecs.open('test.txt', 'w', 'utf8')

cardinfo = {}
flag = 0
index = 0


for item in soup.select('table[cellpadding="3"] tr'):
	if flag == 0:
		flag += 1
		continue
	
	temp = item.text.split('\n')
	cardinfo[index] = {}

	cardinfo[index]['card_number']   = temp[1].strip()
	cardinfo[index]['card_name']     = temp[2].strip()
	cardinfo[index]['card_type']	 = temp[3].strip()
	cardinfo[index]['card_mana']	 = temp[4].strip()
	cardinfo[index]['card_rarity']   = temp[5].strip()
	cardinfo[index]['card_painter']  = temp[6].strip()

	cardinfo[index]['card_language'] = 'en'
	cardinfo[index]['card_set']      = 'bfz'
	cardinfo[index]['card_image']    = 'http://magiccards.info/scans/en/bfz/%s.jpg'%cardinfo[index]['card_number']
	cardinfo[index]['card_color']    = parse_color(cardinfo, index)

	cardinfo[index]['card_subtype']  = ''
	cardinfo[index]['card_value']    = ''

	if '—' in cardinfo[index]['card_type']:
		type_temp = cardinfo[index]['card_type'].split('—')
		cardinfo[index]['card_type'] = type_temp[0].strip()
		cardinfo[index]['card_subtype'] = type_temp[1].strip()

		if 'Creature' in type_temp[0]:
			subtype_temp = type_temp[1].split()
			cardinfo[index]['card_subtype'] = ''
			for subtype in subtype_temp:
				if '/' in subtype:
					cardinfo[index]['card_value'] = subtype
					cardinfo[index]['card_subtype'] = cardinfo[index]['card_subtype'][:-1]
					break

				cardinfo[index]['card_subtype'] += subtype + '|'

	
	f = codecs.open("card_data/bfz/en/%s.html"%(cardinfo[index]['card_number']), 'r', 'utf8')

	content = f.read()

	soup2 = BeautifulSoup(content, 'html.parser')

	f.close()

	
	temp_text = soup2.select('.ctext')[0].text
	temp_text = temp_text.replace("'", "\\'")
	temp_text = temp_text.replace('"', '\\"')
	cardinfo[index]['card_text'] = temp_text
	temp_text = soup2.select('.ctext ~ p')[0].text
	temp_text = temp_text.replace("'", "\\'")
	temp_text = temp_text.replace('"', '\\"')
	cardinfo[index]['card_flavor'] = temp_text
	# print(temp_text)
	#exit()

	index += 1
	
for i in cardinfo:
	temp = 'INSERT INTO cardlist (card_name, card_rarity, card_language, card_color, card_type, card_subtype, card_value, card_mana, card_image, card_text, card_flavor, card_number, card_set, card_painter) VALUES ('
	temp += '"' + cardinfo[i]['card_name'] + '", '
	temp += '"' + cardinfo[i]['card_rarity'] + '", '
	temp += '"' + cardinfo[i]['card_language'] + '", '
	temp += '"' + cardinfo[i]['card_color'] + '", '
	temp += '"' + cardinfo[i]['card_type'] + '", '
	temp += '"' + cardinfo[i]['card_subtype'] + '", '
	temp += '"' + cardinfo[i]['card_value'] + '", '
	temp += '"' + cardinfo[i]['card_mana'] + '", '
	temp += '"' + cardinfo[i]['card_image'] + '", '
	temp += '"' + cardinfo[i]['card_text'] + '", '
	temp += '"' + cardinfo[i]['card_flavor'] + '", '
	temp += '"' + cardinfo[i]['card_number'] + '", '
	temp += '"' + cardinfo[i]['card_set'] + '", '
	temp += '"' + cardinfo[i]['card_painter'] + '");'
	temp += '\n'
	w.write(temp)

print('end')