#!/usr/bin/env python
# coding=utf-8
#全局变量user_mail
from django.http import HttpResponse
from django.conf import settings
def setting(request):
    return {'user_mail': request.session.get('uid', '')}
