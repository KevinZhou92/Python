import urllib
import urllib2
import re
import json
import datetime
import time as counter
import os



class TimeGetter():
	def __init__(self, stop):
		self.stop = stop
		n = datetime.datetime.now()
		t = n.timetuple()
		if (t[3] < 19):
			if stop == 'Thorn Lane':
				self.url = 'https://www.udshuttle.com/Route/4566/Stop/' + '227217' + '/Arrivals?customerID=10'
			elif stop == 'Library' :
				self.url = self.url = 'https://www.udshuttle.com/Route/4566/Stop/' + '227210' + '/Arrivals?customerID=10'
		else :
			if stop == 'Thorn Lane':
				self.url = 'https://www.udshuttle.com/Route/4555/Stop/' + '227217' + '/Arrivals?customerID=10'
			elif stop == 'Library' :
				self.url = self.url = 'https://www.udshuttle.com/Route/4555/Stop/' + '227210' + '/Arrivals?customerID=10'
	
	def getTime(self):
		try:
			url = self.url
			request = urllib2.Request(url)
			response = urllib2.urlopen(request)	
			temp = json.loads(response.read())
			if self.stop == 'Thorn Lane':	
 				print "Current time :", temp["PredictionTime"]
			print "The next bus", temp["Predictions"][0]["BusName"], "will come at" , self.stop , ":", temp["Predictions"][0]["ArriveTime"]
			return 
		except urllib2.URLError, e:
			print ("Can not get the time", e.reason)
			return


def main():
	while(1): 
		time = TimeGetter('Thorn Lane')
		time.getTime()
		time1 = TimeGetter('Library')
		time1.getTime()
		counter.sleep(60)
		os.system('clear')

main()
print(os.environ)



