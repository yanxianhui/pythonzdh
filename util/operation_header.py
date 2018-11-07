#coding:utf-8
import requests
import json
from util.operation_json import OperetionJson
class OperationHeader:
	def __init__(self,response):
		self.response = json.loads(response)
	def get_response_url(self):
		'''
		获取登录返回的token的url
		'''
		url = self.response['data']['url'][0]
		return url
	def get_cookie(self):
		'''
		获取cookie的jar文件
		'''
		#url = self.get_response_url()+"&callback=jQuery21008240514814031887_1508666806688&_=1508666806689"
		#cookie = requests.get(url).cookies
		cookie = self.response['Data']['AccessToken']
		return cookie

	def write_cookie(self):
		#cookie = requests.utils.dict_from_cookiejar(self.get_cookie())
		cookie=self.get_cookie()
		cookies={
   "apsid":{
    "Authorization": "Bearer %s"%(cookie)
  }
}
		op_json = OperetionJson()
		op_json.write_data(cookies)

if __name__ == '__main__':
	
	url = "http://www.clearbos.cn:81/api/auth/login/signin"
	data = {
		"userAccount":"15890158362",
    "userPassword":"123456",
    "VerificationCode":"259199",
    "EncryptCode":""
	}
	res = json.dumps(requests.post(url,data).json())
	op_header = OperationHeader(res)
	#print(op_header.get_cookie())

	op_header.write_cookie()
