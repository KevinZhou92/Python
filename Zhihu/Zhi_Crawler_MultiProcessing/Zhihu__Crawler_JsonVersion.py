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
from User_Getter import User_Getter
import random

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
		self.client_info = 'monsterzpc@gmail.com'
		self.passwd = 'Zpc920515'
		self.url = 'https://www.zhihu.com/login/email'
		self.target_page = ''
		self.position = 0
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
	
	def get_captcha_url(self):
	    url =  'https://www.zhihu.com' + '/captcha.gif?r=' + str(int(time.time())) + '&type=login'
	    f = request.urlopen(url)
	    with open('./cap.png', 'wb') as image:
	    	image.write(f.read())
	    	image.close()

	def login(self):
		'''
			Execution of login

		'''
		if (self.client_info == '' or self.passwd == '') :
			self.client_info = input('请输入账号:')
			self.passwd = getpass('请输入密码:')

		self.get_captcha_url()

		captcha = input('请输入验证码：')

		if (self.client_info.find("@") != -1) :
			print('''正在使用邮箱登录...\n用户名:'''  + self.client_info+ '\n' + '密码 : ' + len(self.passwd) * '*'+ '\n' )
		else :
			self.url = ''
			print('正在使用手机登录...')

		form = {'_xsrf' : self.get_xsrf(), 
				'password' : self.passwd, 
				'email' : self.client_info,
				'captcha': captcha }
		print(form)

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

	def user_getter(sefl):
		return User_Getter('https://www.zhihu.com/people/xiao-guai-shou-2/activities').urls()

	def profile_collector(self, text_path=None) :
		'''
			main entry for collecting user's profile including id, gender, education, career
		'''
		count = 0
		self.cj.load()
		user_list = []
		# check the source of the data
		if (text_path != None) :
			with open(text_path, 'r') as source_list :
				for line in source_list :
					user_list.append(line.split('\n')[0])
				source_list.close()
		else :
			user_list = []

		initial_time = time.time()
		while(len(user_list) > 0):
			# this try except block is for resuming from the server' shutdown  
			try :
				for item in user_list :
					start_time = time.time()
					user_id = item
					print('=Writing information of [', user_id,']...')
					url = 'https://www.zhihu.com/api/v4/members/' + user_id + '?include=locations%2Cemployments%2Cgender%2Ceducations%2Cbusiness%2Cvoteup_count%2Cthanked_Count%2Cfollower_count%2Cfollowing_count%2Ccover_url%2Cfollowing_topic_count%2Cfollowing_question_count%2Cfollowing_favlists_count%2Cfollowing_columns_count%2Canswer_count%2Carticles_count%2Cpins_count%2Cquestion_count%2Ccommercial_question_count%2Cfavorite_count%2Cfavorited_count%2Clogs_count%2Cmarked_answers_count%2Cmarked_answers_text%2Cmessage_thread_token%2Caccount_status%2Cis_active%2Cis_force_renamed%2Cis_bind_sina%2Csina_weibo_url%2Csina_weibo_name%2Cshow_sina_weibo%2Cis_blocking%2Cis_blocked%2Cis_following%2Cis_followed%2Cmutual_followees_count%2Cvote_to_count%2Cvote_from_count%2Cthank_to_count%2Cthank_from_count%2Cthanked_count%2Cdescription%2Chosted_live_count%2Cparticipated_live_count%2Callow_message%2Cindustry_category%2Corg_name%2Corg_homepage%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics'
					req = request.Request(url)
					raw_data = self.opener.open(req).read()
					json_data = json.loads(raw_data)
					
					# get key and value
					pic_url = json_data["avatar_url"].split('_')[0] + '_xll.jpg'
					number_id = json_data["id"]
					user_name = json_data["name"]
					
					# education
					if ("educations" in json_data) :
						if (len(json_data["educations"]) != 0) :
							if ("school" in json_data["educations"][0]) : 
								university = json_data["educations"][0]["school"]["name"]
							else :
								university = 'None'
							if ("major" in json_data["educations"][0]) :
								major = json_data["educations"][0]["major"]["name"]
							else:
								major = 'None'
						else :
							university = 'None' 
							major = 'None' 

					else :
						university = 'None' 
						major = 'None' 
					
					# employments
					if ("employments" in json_data) :
						if (len(json_data["employments"]) != 0) :
							if ("company" in json_data["employments"][0]) :
								company = json_data["employments"][0]["company"]["name"]
							else :
								company = 'None'
							if ("occupation" in json_data["employments"][0]) :
								occupation = json_data["employments"][0]["job"]["name"]
							else :
								occupation = 'None'
						else :
							company = 'None' 
						occupation = 'None' 
					else : 
						company = 'None' 
						occupation = 'None' 
					
					# location
					if ("locations" in json_data) :	
						if (len(json_data["locations"]) != 0) :

							location = json_data["locations"][0]["name"]
						else :
							location = 'None'
					else :
						location = 'None'	
					
					# business
					if ("business" in json_data ) :
						industry = json_data["business"]["name"]
					else :
						industry = 'None' 
					
					intro = json_data["headline"]
					autobiography = json_data["description"]
					user_type = json_data["type"]
					follower_count = json_data["follower_count"]
					following_count = json_data["following_count"]
					answers_count = json_data["answer_count"]
					articles_count = json_data["articles_count"]
					
					if (json_data["gender"] == 1) :
						gender = 'male'
					else :
						gender = 'female'
				
					data = {
					 		'id' :  number_id,
							'user_id' : user_id,
							'name' : user_name,
							'gender' : gender,
							'university' : university,
							'major' : major,
							'industry' : industry,
							'company' : company,
							'occupation' : occupation,
							'location' : location,
							'intro' : intro,
							'autobiography' : autobiography,
							'user_type' : str(user_type),
							'follower_count' : str(follower_count),
							'following_count' : str(following_count),
							'answer-count' : str(answers_count),
							'articles_count' : str(articles_count)
							}
				
					# process folder
					if not (os.path.exists(os.path.join('./data/' ,user_name))): # check if the folder exists
						os.makedirs(os.path.join('./data/' ,user_name))
					path = os.path.join('./data/' ,user_name) + '/'
				
					# generate store path
					store_path = path + user_id
					# write picture
					with open(store_path + '.png', 'wb') as f:
						f.write(self.bytes_getter(pic_url))
						f.close()
					

					target_page_url = 'https://www.zhihu.com/people/' + user_id + '/activities'
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
					count += 1
					print('Wrote Successfully! Time consumed :','%.2f'%(time.time() - start_time),"seconds. Crawled ",count, "users till now.")
					print('[Total time:', '%.2f'%(time.time() - initial_time),'seconds]')
					if (count % 10 == 0) :
						cool_start = time.time()
						cool_down_time = random.randint(0, 10)
						print('#' * 20,'Cooling down for',cool_down_time,' seconds.','#' * 20)
						time.sleep(cool_down_time)
					time.sleep(1.5)
					# record the position before a exception happens
					self.position = user_id

			except Exception as e:
				print('Error! ', e)

			# recover from exception, resume crawling from last user	
			finally :
				index = user_list.index(self.position) + 1
				user_list = user_list[index:]
				time.sleep(10)
				print('#'*20,'Resuming from server shutdown','#'*20)
			
	# for retrieving document		
	def unicode_getter(self, target_url) :
		return self.opener.open(target_url).read().decode('utf-8')

	# for retrieving bytes such as pics
	def bytes_getter(self, target_url) :
		return self.opener.open(target_url).read()


# record ruuning time of program
start_time = time.time()
Zhihu = Zhihu()
Zhihu.login()
#Zhihu.profile_collector('./user_list.txt')
end_time = time.time()
print("[Totally elapsed: " , '%.2f'%(end_time - start_time), " seconds.]")
