#!/usr/bin
# --*-- coding:utf-8 --*--
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

import re
from urllib import parse, request, error
from multiprocessing import Pool
import http.cookiejar as Cookie
import time
import json
from getpass import getpass
import ssl
# Cancel the certification of target site
ssl._create_default_https_context = ssl._create_unverified_context

headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36 ",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Host": "www.zhihu.com",
        "Upgrade-Insecure-Requests": "1",
    }
cookieFile = 'zhihu_cookie.txt'


class RedirectHandler(request.HTTPRedirectHandler):
	def http_error_302(self, req, fp, code, msg, headers):
		print ("Cookie过期，重新登录中....")
		return
	http_error_301 = http_error_302

class Zhihu_Login(object):
	def __init__(self) :		
		self.pool = Pool(4)
		self.cj = Cookie.MozillaCookieJar(cookieFile)
		self.opener = request.build_opener(request.HTTPCookieProcessor(self.cj), RedirectHandler())
		self.user_info = '498956280@qq.com'
		self.passWord = ''
		self.url = 'https://www.zhihu.com/login/email'
		print('''
				############################################################
				#                                                          #
				#      Zhihu Auto_Login and Crawler by Pengcheng Zhou.     #
				#                                                          #
				############################################################
			   ''')
		

	def get_xsrf(self) :
		"""Get a special dynamic string for login"""
		login_page = request.urlopen(self.url)
		pattern = re.compile('<input type="hidden" name="_xsrf" value="(.*)"/>')
		_xsrf = re.findall(pattern, login_page.read().decode('utf-8'))[0]
		return _xsrf

	def login(self):
		"""
		Execution of login

		"""
		
		if (self.user_info == '' or self.passWord == '') :
			self.user_info = input('请输入账号:')
			self.passWord = getpass('请输入密码:')

		if (self.user_info.find("@") != -1) :
			print('''正在使用邮箱登录...\n用户名:'''  + self.user_info+ '\n' + '密码 : ' + len(self.passWord) * '*'+ '\n' )
		else :
			self.url = ''
			print('正在使用手机登录...')

		form = {'_xsrf' : self.get_xsrf(), 
				'password' : self.passWord, 
				'remember_me': 'true',
				'email' : self.user_info }
		
		try:
			req = request.Request(self.url, parse.urlencode(form).encode('utf-8'))
			f = self.opener.open(req)
			self.cj.save()
			print(json.loads(f.read().decode('utf-8'))["msg"] + "!")
			print("=" * 100)
		except:
			print('Error!')
	
	def get_capthca(self) :
		"""
		Interface for get the captcha
		"""
		pass

	def get_page(self):
		"""
		Get main page content after logged in
		"""
		try:
			self.cj.load()
			print('Cookie loaded....')
			log_info = self.opener.open('https://www.zhihu.com/settings/profile')
			page_content = self.opener.open('https://www.zhihu.com/people/edit')
			f = open('zhihu.html', 'wb')
			f.write(page_content.read())
				
		except:
			self.login()
			self.get_page()
			                                                              																						          

temp = Zhihu_Login()


temp.login()

