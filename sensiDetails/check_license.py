#!/usr/bin/env python
# coding=utf-8
from sensiDetails.models import license

class check_license(object):
	"""docstring for check_license"""
	def __init__(self):
		pass
		print 'ok'
	def check_license(self):
		mail_list = ['admin@qq.com']
		license_list = license.objects.all().values('username')
		for v in license_list:
			# print v['username']
			mail_list.append(v['username'])
		return mail_list

