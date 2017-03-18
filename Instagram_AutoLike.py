#!/usr/bin/python
# --*-- encoding:utf-8 --*--
#################################################### 
#               Zhihu Auto-Aogin
# 
#
# Created on : 03/07/17
# Last Modified :   
#
# Author : Pengcheng Zhou(Kevin)
# 
####################################################
import os
from urllib import parse, request, error
import http.cookiejar as Cookie
import time
import json
import re
import ssl 
# Cancel the certification of target site
ssl._create_default_https_context = ssl._create_unverified_context
import zlib


pic_list = []

def test():
	url = 'https://www.instagram.com/'
	f = request.urlopen(url)
	print(f.info())

	for item , v in f.info():
		print(v)

	
class Instagram(object):
	"""docstring for Instagram"""
	def __init__(self):
		self.cj = Cookie.MozillaCookieJar(cookieFile)
		self.opener = request.build_opener(request.HTTPCookieProcessor(self.cj))
		
	def login(self):
		url = 'https://www.instagram.com/accounts/login/ajax/'
		form_data = {'username':'', 'password':''}
		req = request.Request(url, parse.urlencode(form_data).encode('utf-8'),headers=headers)
		f = self.opener.open(req)
		self.cj.save()
		print(f.read())
		print(f.getcode())

	def main_page(self):
		url = 'https://www.instagram.com/zhaoyisha/?__a=1'
		f = self.opener.open(url)
		print(f.read())


		#raw_data = zlib.decompress(f.read(), 32+zlib.MAX_WBITS)
	
	def like(self):
		form_data = {'q':'''ig_user(499296949) { media.after(1448592969321334107, 1200) {count,
		nodes {
		__typename,
		caption,
		code,
		comments {
		count
		},
		    comments_disabled,
		    date,
		    dimensions {
		      height,
		      width
		    },
		    display_src,
		    id,
		    is_video,
		    likes {
		      count
		    },
		    owner {
		      id
		    },
		    thumbnail_src,
		    video_views
		  },
		  page_info
		}
		 }''',
		'ref':'users::show',
		'query_id':'17849115430193904'}
		url = 'https://www.instagram.com/query/?hl=en'
		headers = {
					'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
					'origin':'https://www.instagram.com',
					'referer':'https://www.instagram.com/p/BPfYi-gg2kb/?taken-by=kevinzh92&hl=en',
					'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
					'content-type':'application/x-www-form-urlencoded',
				}
		req = request.Request(url, data = parse.urlencode(form_data).encode('utf-8'), headers=headers)
		f = request.urlopen(req)
		json_data = json.loads(f.read())
		for item in json_data['media']['nodes']:
			pic_id = item['id']
			pic_list.append(pic_id)
		print(len(pic_list))
		
		count = 0
		while(len(pic_list) > 0):
			try:
				for pic in pic_list:
					count += 1
					url = 'https://www.instagram.com/web/likes/' + pic +'/like/'
					form_data = {'hl':'en'}
					req = request.Request(url, headers=headers, data=parse.urlencode(form_data).encode('utf-8'), method='POST')
					f = request.urlopen(req)
					time.sleep(5)
					print(f.read())
					if (count % 20 == 0):		
						print('-------------Liked [',count,']-------------')
			except Exception as e:
				print(e)

temp = Instagram()
temp.like()