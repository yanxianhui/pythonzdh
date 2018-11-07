#coding:utf-8
import sys
sys.path.append("E:/www/ImoocInterface")
from base.runmethod import RunMethod
from data.get_data import GetData
from util.common_util import CommonUtil
from data.dependent_data import DependdentData
from util.send_email import SendEmail
from util.sendemail import Email
from util.operation_header import OperationHeader
from util.operation_json import OperetionJson
from log.user_log import UserLog
class RunTest():
	def __init__(self):
		self.run_method = RunMethod()
		self.data = GetData()
		self.com_util = CommonUtil()
		self.send_mai = SendEmail()  #不带文件发送
		self.send_email=Email()  #带文件发送
		get_user_log=UserLog()
		self.logger = get_user_log.get_log()
	#程序执行的
	def go_on_run(self):
		res = None
		pass_count = []
		fail_count = []
		#10  0,1,2,3
		rows_count = self.data.get_case_lines()
		for i in range(1,rows_count):
			is_run = self.data.get_is_run(i)
			if is_run:
				url = self.data.get_request_url(i)
				method = self.data.get_request_method(i)
				request_data = self.data.get_data_for_json(i)
				expect = self.data.get_expcet_data(i)
				header = self.data.is_header(i)
				depend_case = self.data.is_depend(i)
				case_name=self.data.get_case_name(i)
				if depend_case != None:
					self.depend_data = DependdentData(depend_case)
					#获取的依赖响应数据
					depend_response_data = self.depend_data.get_data_for_key(i)
					#获取依赖的key
					depend_key = self.data.get_depend_field(i)
					request_data[depend_key] = depend_response_data
				if header == 'write':
					res = self.run_method.run_main(method,url,request_data)
					op_header = OperationHeader(res)
					op_header.write_cookie()

				elif header == 'yes':
					op_json = OperetionJson('./dataconfig/cookie.json')
					cookie = op_json.get_data('apsid')
					# cookies = {
					# 	'apsid':cookie
					# }
					res = self.run_method.run_main(method,url,request_data,cookie)
					self.logger.info("用例名称:"+case_name+"--->返回值:"+res)
					#print(res)
				else:
					res = self.run_method.run_main(method,url,request_data)
					self.logger.info("用例名称:" + case_name + "--->返回值:" + res)
					#print(res)
				if self.com_util.is_contain(expect,res) == True:
					self.data.write_result(i,'pass')
					pass_count.append(i)
				else:
					self.data.write_result(i,res)
					fail_count.append(i)
		self.send_mai.send_main(pass_count,fail_count)  #不带文件发送
		#self.send_email.sendemail(pass_count,fail_count)   #不带文件发送


	#将执行判断封装
	#def get_cookie_run(self,header):


if __name__ == '__main__':
	run = RunTest()
	run.go_on_run()
	# RunTest('test_go_on_run')

