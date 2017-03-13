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
import multiprocessing 


cookieFile = 'zhihu_cookie.txt'


class Zhihu(object):
	def __init__(self) :
		'''
			Initialize
		'''		
		self.cj = Cookie.MozillaCookieJar(cookieFile)
		self.opener = request.build_opener(request.HTTPCookieProcessor(self.cj))
		self.client_info = ''
		self.passwd = ''
		self.url = 'https://www.zhihu.com/login/email'
		self.target_page = ''
		self.position = 0
		self.cj.load()
		print('''
				############################################################
				#                                                          #
				#              Zhihu Crawler by Pengcheng Zhou.            #
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

	def profile_collector(self, input_id) :
		'''
			main entry for collecting user's profile including id, gender, education, career
		'''

		start_time = time.time()
		user_id = input_id
		#print('#Writing information of [', user_id,']...')
		try :
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
		    
			#print('Wrote Successfully! Time consumed :','%.2f'%(time.time() - start_time),"seconds.")
		except Exception as e :
			pass
		
		# record the position before a exception happens

	# for retrieving document		
	def unicode_getter(self, target_url) :
		return self.opener.open(target_url).read().decode('utf-8')

	# for retrieving bytes such as pics
	def bytes_getter(self, target_url) :
		return self.opener.open(target_url).read()


# record ruuning time of program
Zhihu = Zhihu()
user_list = []

# read in initial user_list
with open('./user_list.txt', 'r') as f:
	for line in f :
		user_list.append(line.split('\n')[0])
	f.close()

def process_crawler():
	count = 0
	process = []
	start_time = time.time()
	num_cpus = multiprocessing.cpu_count()
	print('Starting number of process : ', num_cpus)

	while (len(user_list) > 0) :
		for i in range(8) :
			p = multiprocessing.Process(target=Zhihu.profile_collector,args=(user_list.pop(0),)) # create a process
			p.daemon = True
			p.start() 
			process.append(p) # add into queue

		for p in process :
			p.join() # waiting for process to join
			count += 1
			if (count % 100 == 0) :
				print('[######### Each operation cost :', '%.2f'%((time.time() - start_time) / count), ' seconds. ##########]')

		process = []
		print('Already crawled : [', count , '] Users.>')
		time.sleep(random.randint(0, 2))
		print('[######### Time elapse :', '%.2f'%(time.time() - start_time), ' seconds. #########]')
		
process_crawler()
print("[Totally elapsed: " , '%.2f'%(end_time - start_time), " seconds.]")
