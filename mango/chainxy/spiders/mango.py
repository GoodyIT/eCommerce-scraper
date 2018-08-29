# from __future__ import unicode_literals
import scrapy

import json

import csv

import os
import signal

import scrapy

from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.conf import settings
from scrapy.http import Request

from chainxy.items import ChainItem

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup as BSoup

import random
import redis

from lxml import etree

import requests
from bs4 import BeautifulSoup

import time

import sys

import pdb

class mango(scrapy.Spider):

	name = 'mango'

	domain = 'https://shop.mango.com/fr'

	url = 'https://shop.mango.com/chequeRegalo.faces?ts=1534505876090&state=she_011_FR'
	
	code_list_path = ''
	proxy_list_path = './data/proxy_list.txt'
	proxy_list = []
	code_list = []

	valid_cnt = 0
	expired_cnt = 0

	previous_code = ''

	form_data = {
		'SVBody:FConsulta:SVCheque3:numero': '',
		'_mng_dialogVisible_panelConsulta': 'false',
		'_mng_panelXY_panelConsulta': '750_400',
		'SVBody:FConsulta_SUBMIT': '1',
		'javax.faces.ViewState': '',
		'_mng_hidde_valuej_id_4e': 'j_id_4e',
		'javax.faces.behavior.event': 'click',
		'javax.faces.partial.event': 'click',
		'javax.faces.source': 'SVBody:FConsulta:SVCheque3:j_id_4e',
		'javax.faces.partial.ajax': 'true',
		'javax.faces.partial.execute': 'SVBody:FConsulta',
		'javax.faces.partial.render': 'SVBody:FConsulta:SVCheque3:errorVale SVBody:FConsulta:SVCheque3:SVCheque5:panelConsultaSaldo',
		'SVBody:FConsulta': 'SVBody:FConsulta'
	}

	cookies = {
		'mangoShopCookie':	'FR_011____001_001_she___FGL3FUJHM65ARPIPSM7I53QA',
		'mangoShopCookie_Version':	'v4',
		'googleexperiments':	'f7vvksYoT6qgQMqXyi1ECw%3A1%2Cmh12LpHoRj6DNGS2-1SrAw%3A1%2C',
		'mangoShopCookie_Banner':	'.aleatorio-b',
		'_ga':	'GA1.3.501232986.1534142176',
		'_ga':	'GA1.2.501232986.1534142176',
		'_gaexp':	'GAX1.2.8cyHxb2IQzKFQiF1EmZIlQ.17824.1',
		'cto_lwid':	'eef2bef7-da1e-4259-b743-acb449ce3a5e',
		'_msuuid_7iu9q7bk10':	'7CFAD67D-1211-47CA-A3E0-A5BCF4584734',
		'MNGSESSIONID':	'5772A8B1A01F370C0C9E2B1F72BABE26',
		'AWSELB':	'BFC5C7171EE3DEE8EF093B004B4B9C189E4132CE5264D17DB4247A6C05E7508ECC1B008D652D79498A153394E254D79A884D0DDEE338369A7D1634BCF9806EB736A1E52A3F404D12FB11814323B21DE78076C5ABE2',
		'_gid':	'GA1.2.774278676.1534410148',
		'_gid':	'GA1.3.774278676.1534410148',
		'mangoShopBannerCookiesShown':	'true',
		'modalRegistroNewsletter':	'0',
		'kidsNavigationCookie':	'"eyJwcmV2aW91c05hdmlnYXRpb25HaXJsIjoiIiwicHJldmlvdXNOYXZpZ2F0aW9uQm95IjoiIn0=  "',
		'_gat':	'1',
		'firstVisit':	'false',
		'_dc_gtm_UA-855910-3':	'1',
		'_gat_UA-855910-26':	'1',
		'oam.Flash.RENDERMAP.TOKEN':	'-1det4ceuho',
		'shopCookie': 'null',
		'dtCookie': '|U2hvcHww',
		'__sonar': '11559243430523979154'
	}

	headers = {
		':authority': 'shop.mango.com',
		':method': 'POST',
		':path': '/chequeRegalo.faces?ts=1534505876090&state=she_011_FR',
		'scheme:': 'https',
		'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'accept-encoding': 'gzip, deflate, br',
		'content-type':' application/x-www-form-urlencoded; charset=UTF-8',
		'faces-request': 'partial/ajax',
		'origin': 'https://shop.mango.com',
		'referer': 'https://shop.mango.com/chequeRegalo.faces',
		'cookie': 'mangoShopCookie_Version=v4; googleexperiments=mh12LpHoRj6DNGS2-1SrAw%3A1%2C; _ga=GA1.2.403679940.1534004018; mangoShopCookie_Banner=.aleatorio-b; _ga=GA1.3.403679940.1534004018; _gaexp=GAX1.2.8cyHxb2IQzKFQiF1EmZIlQ.17824.1; cto_lwid=1252b18e-7130-4bd7-a3e7-7a783a007f81; _msuuid_7iu9q7bk10=7CFAD67D-1211-47CA-A3E0-A5BCF4584734; __utma=76354697.403679940.1534004018.1534011834.1534011834.1; __utmz=76354697.1534011834.1.1.utmcsr=shop.mango.com|utmccn=(referral)|utmcmd=referral|utmcct=/iframe.faces; _gid=GA1.2.504914928.1534273650; _gid=GA1.3.504914928.1534273650; dtCookie=|U2hvcHww; MNGSESSIONID=E3BD4DC70FB0C1C8466080EA227C9DE7; mangoShopBannerCookiesShown=true; modalRegistroNewsletter=0; shopCookie=null; sb_user_id=123b3f5a-2fb0-4a04-8ff1-ece395334282; kidsNavigationCookie="eyJwcmV2aW91c05hdmlnYXRpb25HaXJsIjoiIiwicHJldmlvdXNOYXZpZ2F0aW9uQm95IjoiIn0=  "; mangoShopCookie=FR_011____001_001_nina___FGL3FUJHM65ARPIPSM7I53QA; AWSELB=BFC5C7171EE3DEE8EF093B004B4B9C189E4132CE52A3F5E341F7834220A60DC64DCC28011203435B685B7153A43F9C26EDD9B5DFC338369A7D1634BCF9806EB736A1E52A3F16D2F159017CEC20F1AD642B63470873; _gat=1; _dc_gtm_UA-855910-3=1; _gat_UA-855910-26=1; oam.Flash.RENDERMAP.TOKEN=14r68oedtt; firstVisit=false',
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
	}

	def __init__(self, _code_list_path='', _proxy_list_path ='', _concurrent_requests=32):
		super(mango, self).__init__()
		print('========== code list path =======', _code_list_path)
		self.code_list_path = _code_list_path	
		self.proxy_list_path = _proxy_list_path

		# initialize redis
		self.r = redis.StrictRedis(host='localhost', port=6379, db=0)
		self.p = self.r.pubsub()
		# self.p.subscribe(**{'scrapy-channel': self.my_handler})
		# self.p.run_in_thread(sleep_time=0.001)

		option = webdriver.ChromeOptions()
		option.add_argument('headless')
		option.add_argument('blink-settings=imagesEnabled=false')
		option.add_argument('--ignore-certificate-errors')
		option.add_argument('--ignore-ssl-errors')
		option.add_argument("--no-sandbox")
		option.add_argument("--disable-impl-side-painting")
		option.add_argument("--disable-setuid-sandbox")
		option.add_argument("--disable-seccomp-filter-sandbox")
		option.add_argument("--disable-breakpad")
		option.add_argument("--disable-client-side-phishing-detection")
		option.add_argument("--disable-cast")
		option.add_argument("--disable-cast-streaming-hw-encoding")
		option.add_argument("--disable-cloud-import")
		option.add_argument("--disable-popup-blocking")
		option.add_argument("--disable-session-crashed-bubble")
		option.add_argument("--disable-ipv6")

		self.driver = webdriver.Chrome(executable_path='./data/chromedriver.exe', chrome_options=option)

		# change concurrent threads in setting.py
		settings.set('CONCURRENT_REQUESTS', _concurrent_requests)

	# def my_handler(self, message):
	# 	if 'stop' in json.loads(message['data']):
	# 		# raise scrapy.exceptions.CloseSpider('Manually stopped')
	# 		os.kill(os.getpid(), signal.CTRL_C_EVENT)
	# 	else:
	# 		print('-------------- error in my_handler in scraper --------------')

	# def closed( self, reason ):
	# 	print('--------- spider closed ------------:', reason)
	# 	self.r.publish('scrapy-channel', json.dumps({'exit': '1'}))

	def start_requests(self):
    		
        # read the code list from the file
		with open(self.code_list_path, 'rb') as text:
			conent = text.readlines()
			for code in conent:
				self.code_list.append(code.replace('\n', '').replace('\r', ''))

		# get proxy from file
		with open(self.proxy_list_path, 'rb') as text:
			content = text.readlines()
			for proxy in content :
				proxy = proxy.replace('\n', '')
				self.proxy_list.append(proxy)
		
		# option.add_experimental_option("detach", True)
		yield Request("https://stackoverflow.com/", callback=self.parse_dummy)
		
	def parse_dummy(self, response):
		self.driver.get("https://shop.mango.com/fr")
		# WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "he"))).click()
	
		WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='icon closeModal icon__close desktop confirmacionPais']"))).click()

		WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[@id='cheques']/a"))).click()

		# got to WHAT IS THE BALANCE OF MY GIFT CERTIFICATE? option
		WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "SVBody:SVCheque4:FMenu:j_id_2y"))).click()
		# wait until loaded
		time.sleep(1)

		# read the pause point
		self.pipeline = open("data/pipeline.dat","r")
		read_value = self.pipeline.readlines()
		if len(read_value) == 0:
			start_index = 0
		else:
			start_index = int(read_value[0].split(",")[2].replace('\n', ''))
			self.valid_cnt = int(read_value[0].split(",")[0].replace('\n', ''))
			self.expired_cnt = int(read_value[0].split(",")[1].replace('\n', ''))

		self.cookie_temp = self.driver.get_cookies()
		url = etree.HTML(self.driver.page_source).xpath('//form[@id="SVBodyHeader:SVUserMenu:userMenuForm"]/@action')[0]
		# self.driver.close()
		view_state= etree.HTML(self.driver.page_source).xpath('//input[@name="javax.faces.ViewState"]/@value')[0]
		for x in range(start_index, len(self.code_list)):
			self.form_data['SVBody:FConsulta:SVCheque3:numero'] = self.code_list[x]
			self.form_data['javax.faces.ViewState'] = view_state
			self.headers[':path'] = '/chequeRegalo.faces?' + url.split('?')[1]
			request = scrapy.FormRequest(url, callback=self.parse_case, headers=self.headers, formdata=self.form_data, cookies=self.cookie_temp, meta={'proxy' : random.choice(self.proxy_list)})
			# request = scrapy.FormRequest(url, callback=self.parse_case, headers=self.headers, formdata=self.form_data, cookies=self.cookie_temp)
			request.meta['code'] = self.code_list[x]
			request.meta['index'] = x
			
			yield request

	def parse_case(self, response):
		if len(response.xpath("//update")) == 0:
			print("# timestamp is expired so need to go back to the first stage again ************************")
			# self.pipeline.write(str(self.valid_cnt)+","+str(self.expired_cnt)+","+response.meta['index'])
			# self.pipeline.close()
			# # stop spider and restart it again
			# self.r.publish('scrapy-channel', json.dumps({'timestamp': '1'}))
			# raise scrapy.exceptions.CloseSpider('timestamp expired')
			yield Request("https://stackoverflow.com/", callback=self.parse_dummy)
			return
    				
		table = etree.HTML(response.body).xpath(".//table//span")
		# pdb.set_trace()
		print('-----------', response.meta['code'] )
		self.previous_code = response.meta['code']
		item = ChainItem()
		try:
			item['code'] = self.validate( table[0].xpath('.//text()')[0])
			item['balance'] =  self.validate(table[1].xpath('.//text()')[0])
			item['validation_date'] =  self.validate(table[2].xpath('.//text()')[0])
			self.valid_cnt += 1
		except:
			print('--------------------- invalid code -----------------------')
			self.expired_cnt += 1
			item['code'] = response.meta['code']
			item['balance'] = -1
			item['validation_date'] = 'invalid'

		# publish the status of processing code
		redis_output = {
			'code': response.meta['code'],
			'valid_cnt': self.valid_cnt,
			'expired_cnt': self.expired_cnt,
			'total_cnt': self.valid_cnt+self.expired_cnt,
			'index':response.meta['index']
		}

		self.r.publish('scrapy-channel', json.dumps(redis_output))

		yield item

	def validate(self, value):
		return value.encode('utf-8').replace('\xe2\x82\xac', '')
