
from urllib import request
import codecs
import json
from io import StringIO
import gzip
import zlib
import time
import ssl 
import ssl 
# Cancel the certification of target site
ssl._create_default_https_context = ssl._create_unverified_context

headers = {"accept":"*/*",
			"Accept-Encoding":"gzip, deflate, sdch, br",
			"Accept-Language":"en-GB,en;q=0.8,en-US;q=0.6,zh-CN;q=0.4,zh;q=0.2",
			"authorization":"oauth c3cef7c66a1843f8b3a9e6a1e3160e20",
			"Connection":"keep-alive",
			"Host":"www.zhihu.com",
			"Referer": "https://www.zhihu.com/people/he-xie-52-94/asks",
			"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"	
			}	    

url = 'https://www.zhihu.com/api/v4/members/Mr.DongDong?include=locations%2Cemployments%2Cgender%2Ceducations%2Cbusiness%2Cvoteup_count%2Cthanked_Count%2Cfollower_count%2Cfollowing_count%2Ccover_url%2Cfollowing_topic_count%2Cfollowing_question_count%2Cfollowing_favlists_count%2Cfollowing_columns_count%2Canswer_count%2Carticles_count%2Cpins_count%2Cquestion_count%2Ccommercial_question_count%2Cfavorite_count%2Cfavorited_count%2Clogs_count%2Cmarked_answers_count%2Cmarked_answers_text%2Cmessage_thread_token%2Caccount_status%2Cis_active%2Cis_force_renamed%2Cis_bind_sina%2Csina_weibo_url%2Csina_weibo_name%2Cshow_sina_weibo%2Cis_blocking%2Cis_blocked%2Cis_following%2Cis_followed%2Cmutual_followees_count%2Cvote_to_count%2Cvote_from_count%2Cthank_to_count%2Cthank_from_count%2Cthanked_count%2Cdescription%2Chosted_live_count%2Cparticipated_live_count%2Callow_message%2Cindustry_category%2Corg_name%2Corg_homepage%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics'
req = request.Request(url,None, headers)
page = request.urlopen(req)
raw_data = zlib.decompress(page.read(), 32+zlib.MAX_WBITS)
count = 10
if (count % 10 == 0):
	cool_start = time.time()
	print(time.sleep(10))
	print(time.time() - cool_start)
	#print(json.loads(raw_data))

