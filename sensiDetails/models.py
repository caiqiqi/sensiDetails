# coding=utf-8
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class SensiDetails(models.Model):
    id         =  models.AutoField(primary_key=True, verbose_name='自增主键') #主键
    status     =  models.IntegerField(verbose_name='当前状态') # 0: 已处理 1: 未处理 2: 忽略
    title      =  models.CharField(max_length=255,null=True,blank=True, verbose_name='标题')
    url        =  models.CharField(max_length=255,null=True,blank=True, verbose_name='url')
    details    =  models.TextField(verbose_name='摘要')  # 摘要
    create_time=  models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time=  models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __unicode__(self): # __str__ , 大坑-https://blog.csdn.net/lmz_lmz/article/details/80088580 
        return u'%s %s %s %s %s ' %  (self.id, self.status, self.title, self.url, self.details)

class license(models.Model):
    username = models.CharField(max_length=255,null=True,blank=True) #授权用户
