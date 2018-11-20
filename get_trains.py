#-*- encoding:utf-8 -*-

'''
通过http请求获取前信发布的接口数据
'''

import urllib2
import urllib
import json
import time

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def train_list():
	src_url = "http://10.81.33.151/api/oauth/token"
	Authorization = 'Basic bXktdHJ1c3RlZC1jbGllbnQ6c2VjcmV0'

	headers = {'Authorization': Authorization}
	data = {'grant_type': 'password', 'username': 'admin', 'password': 'admin2018'}
	data = urllib.urlencode(data)

	request = urllib2.Request(url=src_url, data=data, headers=headers)
	try:
		response = urllib2.urlopen(request)
	# print response.read()
	except Exception, e:
		print "Error:", e

	response_data = response.read()
	access_token = eval(response_data)['access_token']

	#print access_token

	# temp_url = 'http://10.81.33.154:8080/api/service/train_recent'
	#temp_url = 'http://10.81.33.154:8080/api/service/passenger_front_16'  # 16小时内列车车次信息接口
	#temp_url = 'http://10.81.33.154:8080/api/service/passenger_zw'  # 16小时内列车车次信息接口
	#temp_url = 'http://10.81.33.151:8080/api/service/monitoringLEDScreen'  #2018-04-26最新旅服到发接口
	temp_url = 'http://10.81.33.151:8080/api/service/nextTwelveHourTrain'
	paras = {"access_token": access_token, "pageSize": 150}
	paras = urllib.urlencode(paras)
	dest_url = temp_url + "?" + paras
	request = urllib2.Request(dest_url)
	response = urllib2.urlopen(request)
	train_info = response.read().decode('utf-8')
	print train_info
	with open('C:/Users/hzy/Desktop/train_info.txt','wb') as f:
		f.write(train_info)

	train_info_dict = {}
	train_info_dict = json.loads(train_info)
	train_info_dict = train_info_dict['data']['list']
	train_info_dict_sort = sorted(train_info_dict,key = lambda train_info_dict:train_info_dict['DEPARTURE_TIME'])
	#train_info_dict_sort = set(train_info_dict_sort)
	#print train_info_dict_sort
	room1 = []
	room2 = []
	room3 = []
	room4 = []
	realtime = time.strftime('%Y-%m-%d %H:%M:%S.0')
	for i in train_info_dict_sort:
		if i['REAL_WAIT_NAME'] in [u'\u7b2c\u4e00\u5019\u8f66\u5ba4',u'\u7b2c\u4e00\u5019\u8f66\u5ba4\u002c\u7b2c\u4e8c\u5019\u8f66\u5ba4'] and i['TRAIN_TYPE'] <> "2" and i['DEPARTURE_TIME'] > realtime:
			if i['DEPARTURE_TRAIN_CODE'] == 'K7808':
				room1.append(i['DEPARTURE_TRAIN_CODE']+'(8-17)')
				room2.append(i['DEPARTURE_TRAIN_CODE']+'(1-7)')
			else:
				room1.append(i['DEPARTURE_TRAIN_CODE'])		
		elif i['REAL_WAIT_NAME'] == [u'\u7b2c\u4e8c\u5019\u8f66\u5ba4'] and i['TRAIN_TYPE'] <> "2" and i['DEPARTURE_TIME'] > realtime:
			room2.append(i['DEPARTURE_TRAIN_CODE'])
		elif i['REAL_WAIT_NAME'] == u'\u7b2c\u4e09\u5019\u8f66\u5ba4' and i['TRAIN_TYPE'] <> "2" and i['DEPARTURE_TIME'] > realtime:
			room3.append(i['DEPARTURE_TRAIN_CODE'])
		elif i['REAL_WAIT_NAME'] == u'\u7b2c\u56db\u5019\u8f66\u5ba4' and i['TRAIN_TYPE'] <> "2" and i['DEPARTURE_TIME'] > realtime:
			room4.append(i['DEPARTURE_TRAIN_CODE'])


	train_list = {}
	train_list[1] = []
	train_list[2] = []
	train_list[3] = []
	train_list[4] = []
	if len(room1) < 9:
		train_list[1].extend(room1)
		#print u"第一候车室：{}".format(room1)
	else:
		train_list[1].extend(room1[0:8])
		#print u"第一候车室：{}".format(room1[0:8])
	if len(room2) < 11:
		train_list[2].extend(room2)
		#print u"第二候车室: {}".format(room2)
	else:
		train_list[2].extend(room2[0:10])
		#print u"第二候车室: {}".format(room2[0:10])
	if len(room3) < 11:
		train_list[3].extend(room3)
		#print u"第三候车室: {}".format(room3)
	else:
		train_list[3].extend(room3[0:10])
		#print u"第三候车室: {}".format(room3[0:10])
	if len(room4) < 11:
		train_list[4].extend(room4)
		#print u"第四候车室: {}".format(room4)
	else:
		train_list[4].extend(room4[0:10])
		#print u"第四候车室：{}".format(room4[0:10])
	return train_list

if __name__ == "__main__":
	print train_list()