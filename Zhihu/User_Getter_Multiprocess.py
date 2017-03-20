from urllib import request
import codecs
import json
import gzip
import zlib
import time
import ssl 
# Cancel the certification of target site
ssl._create_default_https_context = ssl._create_unverified_context


class User_Getter(object):
	"""
		docstring for Url_Getter
		This class get all the urls of following users
	"""
	
	def __init__(self, sourceUrl):
		self.src_url = sourceUrl
		self.headers = {
        "accept":"application/json, text/plain, */*",
		"Accept-Encoding":"gzip, deflate, sdch, br",
		"Accept-Language":"en-GB,en;q=0.8,en-US;q=0.6,zh-CN;q=0.4,zh;q=0.2",
		"authorization":"oauth c3cef7c66a1843f8b3a9e6a1e3160e20",
		"Connection":"keep-alive",
		"Host":"www.zhihu.com",
		"Referer": "https://www.zhihu.com/people/he-xie-52-94/asks",
		"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"		    
    }

	def urls(self) :
		'''
			start from source url to retrieve all the following the current user has
			Here we use following instead of followers to avoid of getting too many zombie links
			# here we implement Breadth-First Search to retrieve the cloest users
		'''
		user_list = []
		queue = []
		# starting user
		user_id = self.src_url.split('/')[4:5][0]
		queue.append(user_id)
		# request data
		i = 0
		initial_time = time.time()
		while(len(queue) > 0 and len(user_list) < 10000000) :
			try :
				size = len(queue)
				while (size > 0 ):
					size -= 1
					user_id = queue.pop(0)
					url = 'https://www.zhihu.com/api/v4/members/' + user_id +'/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=0&limit=1000'
					req = request.Request(url,None, self.headers)
					resopnse = request.urlopen(req)
					raw_data = zlib.decompress(resopnse.read(), 32+zlib.MAX_WBITS)
					json_data = json.loads(raw_data.decode('utf-8'))["data"]
					for item in json_data :
						if (item['url_token'] != None and item['url_token'] not in user_list):
							user_list.append(item['url_token'])
							queue.append(item['url_token'])
							
							# write operation for every [constant number] record in case of shutdown
							if (len(user_list) % 8000 == 0):
								with open('./user_list.txt', 'w') as f :
									for id in user_list :
										f.write(id)
										f.write('\n')
									f.close()
									print('#'*20,'Wrote to file [user_list.txt]','#'*25)
						# print(json_data)
					print('Already crawled ', len(user_list),' records. Finished',len(user_list) * 100/1000000 ,'%.')
					print('[Total time:', '%.2f'%(time.time() - initial_time),'seconds]')
					time.sleep(1)
					
			except Exception as e:
				print("Cannot fetch user " + user_id+ ". ", end='')
				print(e)
				pass
		
		return user_list

	
if __name__ == '__main__':
	start_time = time.time()	
	test_client = User_Getter('https://www.zhihu.com/people/xiao-guai-shou-2/activities')	
	print("[Totally retrieved : ", len(test_client.urls()), " records.]")
	end_time = time.time()	
	print("[Program elapsed : " , '%.2f'%(end_time - start_time), " seconds.]")

