#coding=utf-8

#常用库引用
import urllib
import urllib2
import re
import requests
import time
import socket
import os
import json
import hashlib
import struct
import binascii
import telnetlib
import array

#刷新显示
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

#django response库 
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings


headers={      "User-Agent":"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36",
                "Accept":"*/*",
                "Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
                "Accept-Encoding":"gzip, deflate",
                "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
                "X-Requested-With":"XMLHttpRequest",
                "Connection":"keep-alive"
        }

