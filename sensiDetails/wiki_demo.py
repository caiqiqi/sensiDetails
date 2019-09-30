#coding=utf-8
import warnings,base64,sys,json
import requests

#from db import init, insert
from utils import is_valid_url, is_valid_details, filter_highlight
from mail import send_mail
import models
#from sensiDetails import models

warnings.filterwarnings("ignore")
reload(sys)
sys.setdefaultencoding( "utf-8" )

search = """
"用户名 AND 密码" OR  "默认用户" OR "默认密码" OR "user AND password" OR "admin" -"密码学" -"密码错误"
"""

url = "https://wiki.example.cn/rest/experimental/search?user=sec&cql=siteSearch+~+" + \
"%22%5C%22%E7%94%A8%E6%88%B7%E5%90%8D+AND+%E5%AF%86%E7%A0%81%5C%22+OR++%5C%22%E9%BB%98%E8%AE%A4%E7%94%A8%E6%88%B7%5C%22+OR+%5C%22%E9%BB%98%E8%AE%A4%E5%AF%86%E7%A0%81%5C%22+OR+%5C%22user+AND+password%5C%22+OR+%5C%22admin%5C%22+-%5C%22%E5%AF%86%E7%A0%81%E5%AD%A6%5C%22+-%5C%22%E5%AF%86%E7%A0%81%E9%94%99%E8%AF%AF%5C%22%22" + \
"&start={}&limit=500&excerpt=highlight"

class Wiki(object):
	def __init__(self):
		name = "sec"
		password = "passwrod"
		tmp = name + ':' + password
		auth = base64.b64encode(tmp)
		self.headers = {
                        'X-Atlassian-Token': 'no-check',
			'Authorization': 'Basic'+' '+auth,
		}

	def get_page(self, num=10000):
		result = []
                proxies = {
                        #'http': 'http://192.168.170.1:8087',
                        #'https': 'https://192.168.170.1:8087',
                }
		for i in range(0, num, 500):
			req = requests.get(url.format(str(i)), headers=self.headers, proxies=proxies, verify=False)
                        json_data = json.loads(req.content)
			
			for i in json_data['results']:
				if(is_valid_url(i['url'])  and is_valid_details(i['excerpt']) ) :
					tup = (filter_highlight(i['title']), i['url'], filter_highlight(i['excerpt']))
					result.append(tup)
			
			if len(json_data['results']) < 500:   # 小于500，则可认为已经完成爬取。
				break
		return result

if __name__ == '__main__':
	wiki = Wiki()
	result = wiki.get_page()

	#init()
	#insert(result)
        models.objects.bulk_create(result)   # 批量插入数据
        send_mail(result)   # 将结果发送邮件
