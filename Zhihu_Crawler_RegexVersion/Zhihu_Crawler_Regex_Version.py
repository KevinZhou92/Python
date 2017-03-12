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
import os
import zhihu_regex
from Url_Getter import Url_Getter

cookieFile = 'zhihu_cookie.txt'


class RedirectHandler(request.HTTPRedirectHandler):
	def http_error_302(self, req, fp, code, msg, headers):
		print ("Cookie过期，重新登录中....")
		return
	http_error_301 = http_error_302

class Zhihu(object):
	def __init__(self) :
		'''
			Initialize
		'''		
		self.pool = Pool(4)
		self.cj = Cookie.MozillaCookieJar(cookieFile)
		self.opener = request.build_opener(request.HTTPCookieProcessor(self.cj), RedirectHandler())
		self.client_info = ''
		self.passwd = ''
		self.url = 'https://www.zhihu.com/login/email'
		self.target_page = ''
		print('''
				############################################################
				#                                                          #
				#      Zhihu Auto_Login and Crawler by Pengcheng Zhou.     #
				#                                                          #
				############################################################
			   ''')
		

	def get_xsrf(self) :
		'''
			Get a special dynamic string for login
		'''
		login_target_page = request.urlopen(self.url)
		pattern = re.compile('<input type="hidden" name="_xsrf" value="(.*)"/>')
		_xsrf = re.findall(pattern, login_target_page.read().decode('utf-8'))[0]
		return _xsrf

	def login(self):
		'''
			Execution of login

		'''
		
		if (self.client_info == '' or self.passwd == '') :
			self.client_info = input('请输入账号:')
			self.passwd = getpass('请输入密码:')

		if (self.client_info.find("@") != -1) :
			print('''正在使用邮箱登录...\n用户名:'''  + self.client_info+ '\n' + '密码 : ' + len(self.passwd) * '*'+ '\n' )
		else :
			self.url = ''
			print('正在使用手机登录...')

		form = {'_xsrf' : self.get_xsrf(), 
				'password' : self.passwd, 
				'remember_me': 'true',
				'email' : self.client_info }
		
		try:
			req = request.Request(self.url, parse.urlencode(form).encode('utf-8'))
			f = self.opener.open(req)
			self.cj.save()
			print(json.loads(f.read().decode('utf-8'))["msg"] + "!")
			print("=" * 100)
		except:
			print('Error!')
	
	def get_capthca(self) :
		'''
			Interface for getting the captcha
		'''
		pass

	def get_target_page(self):
		'''
			Get main target_page content after logged in
		'''
		try:
			self.cj.load()
			print('Cookie loaded....')
			self.target_page = self.opener.open('https://www.zhihu.com/people/edit')
			f = open('zhihu.html', 'wb')
			f.write(target_page_content.read())
				
		except:
			self.login()
			self.get_target_page()
	
	def isLogged(self, user_client):
		'''
			test if Logged
		'''
		f = user_client.open('https://www.zhihu.com/settings/profile').geturl()	
		if (f != 'https://www.zhihu.com/settings/profile'):
			return False
		return True	                                                              																						          

	def profile_collector(self, target_page_url=None) :
		self.cj.load()
		'''
			main entry for collecting user's profile including id, gender, education, career
		'''
		user_time = time.time()
		target_page = self.unicode_getter(target_page_url)
		
		#user_id
		user_id = target_page_url.split('/')[4:5][0]
		print('Writing information of [', user_id,']...')
		# user_name
		user_name_pattern = zhihu_regex.pattern_getter('USER_NAME')
		user_name = re.search(user_name_pattern, target_page).group(1)

		# profile_photo
		pic_url_pattern = zhihu_regex.pattern_getter('PHOTO')
		pic_url = re.search(pic_url_pattern, target_page).group(1)
		
		# gender 
		gender_pattern = zhihu_regex.pattern_getter('GENDER')
		gender = re.search(gender_pattern, target_page)
		if (gender == None) :
			gender = None
		elif (gender[4] == 'Icon Icon--female') :
			gender = 'female' 
		else :
			gender = 'male'

		#career_info
		career_pattern = zhihu_regex.pattern_getter('CAREER')
		career_info = re.search(career_pattern, target_page)

		if (career_info): # to aviod users with no career_info
			if (re.search(re.compile('(.*)<div class="ProfileHeader-divider"></div>'), career_info[0])) :
				career_info = career_info[2]
				detail_pattern = zhihu_regex.pattern_getter('CAREER_DETAIL')
				if (re.search(detail_pattern, career_info)) :
					industry = re.search(detail_pattern, career_info)[1]
					company = re.search(detail_pattern, career_info)[2]
					occupation = re.search(detail_pattern, career_info)[3]
				else :
					detail1_pattern = zhihu_regex.pattern_getter('CAREER_DETAIL_1')
					career_info1 = re.search(detail1_pattern, career_info)
					industry = career_info1[1]
					company = career_info1[1]
					occupation = career_info1[2]
			else :
				industry = career_info[2]
				company = 'None'
				occupation = 'None'
		else :
			industry = 'None'
			company = 'None'
			occupation = 'None'


		#education and major
		education_pattern= 	zhihu_regex.pattern_getter('EDUCATION')
		education = re.search(education_pattern, target_page)
		
		if (education == None) :
			university = ''
			major = ''
		else : 
			university = education[2]
			major = education[3]
		

		# intro
		intro_pattern = re.compile('<span class="RichText ProfileHeader-headline">(.*?)</span>')
		intro = re.search(intro_pattern, target_page)
		if (intro == None) :
			intro = 'None'
		else :
			intro = intro[1]
		
		#json file
		data = {
				'id' : user_id,
				'name' : user_name,
				'gender' : gender,
				'university' : university,
				'major' : major,
				'industry' : industry,
				'company' : company,
				'occupation' : occupation,
				'intro' : intro
				}
		
		# process folder
		if not (os.path.exists(os.path.join('./data/' ,user_name))): # check if the folder exists
			os.makedirs(os.path.join('./data/' ,user_name))
		path = os.path.join('./data/' ,user_name) + '/'
	
		# generate store path
		store_path = path + user_name
		# write picture
		with open(store_path + '.png', 'wb') as f:
			f.write(self.bytes_getter(pic_url))
			f.close()
		
		# write target_page
		with open(store_path +'.html', 'wb') as f:
			f.write(self.bytes_getter(target_page_url))
			f.close()

		with open(store_path + '.txt', 'w', encoding='utf-8') as f:
			for item, value in data.items():
				line = json.dumps(item + ":" + value, ensure_ascii=False) + "\n"
				f.write(line)
				#f.write(json.dumps(data, ensure_ascii=False))
			f.close()
			print('Write Successfully! Time :', time.time() - user_time)
			
	# for retrieving document		
	def unicode_getter(self, target_url) :
		return self.opener.open(target_url).read().decode('utf-8')

	# for retrieving bytes such as pics
	def bytes_getter(self, target_url) :
		return self.opener.open(target_url).read()


# record ruuning time of program
start_time = time.time()
Zhihu = Zhihu()

def getter():
	Zhihu.cj.load()
	url = 'https://www.zhihu.com/api/v4/members/xiao-guai-shou-2?include=locations%2Cemployments%2Cgender%2Ceducations%2Cbusiness%2Cvoteup_count%2Cthanked_Count%2Cfollower_count%2Cfollowing_count%2Ccover_url%2Cfollowing_topic_count%2Cfollowing_question_count%2Cfollowing_favlists_count%2Cfollowing_columns_count%2Canswer_count%2Carticles_count%2Cpins_count%2Cquestion_count%2Ccommercial_question_count%2Cfavorite_count%2Cfavorited_count%2Clogs_count%2Cmarked_answers_count%2Cmarked_answers_text%2Cmessage_thread_token%2Caccount_status%2Cis_active%2Cis_force_renamed%2Cis_bind_sina%2Csina_weibo_url%2Csina_weibo_name%2Cshow_sina_weibo%2Cis_blocking%2Cis_blocked%2Cis_following%2Cis_followed%2Cmutual_followees_count%2Cvote_to_count%2Cvote_from_count%2Cthank_to_count%2Cthank_from_count%2Cthanked_count%2Cdescription%2Chosted_live_count%2Cparticipated_live_count%2Callow_message%2Cindustry_category%2Corg_name%2Corg_homepage%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics'
	req = request.Request(url)
	page = Zhihu.opener.open(url)
	print(json.loads(page.read().decode('utf-8')))
getter()

test_url = [
			'https://www.zhihu.com/people/wen-yi-yang-81/activities',
			'https://www.zhihu.com/people/xuan-hun/activities',
			'https://www.zhihu.com/people/xiao-guai-shou-2/activities',
			'https://www.zhihu.com/people/yu-chao-chao-59/answers',
			'https://www.zhihu.com/people/shi-yidian-ban-98/activities'
			]

for url in test_url:
	Zhihu.profile_collector(url)
	time.sleep(0.2)
	pass

end_time = time.time()
print("[Totally elapsed: " , (end_time - start_time), " seconds.]")
