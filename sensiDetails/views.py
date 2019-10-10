# -*- coding: utf-8 -*-
import traceback

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect   # 302跳转

from sensiDetails import models
from .wiki_demo import Wiki
from .mail import send_mail
# Create your views here.

NUM_DATA_PER_PAGE = 20 #每一页多少条数据


def is_login(func):
        def wrapper(request,*args,**kwargs):
                if request.user.is_authenticated:
                        return func(request,*args,**kwargs)
                return HttpResponseRedirect('/admin')
        return wrapper


@is_login
def index(request):
    resp = redirect("/sensi_details/get_list/")  # 302跳转到敏感信息详情页面
    return resp
    #return render(request, 'index.html',{})


# 渲染响应
def render_resp(p_sensiList, p_page):
    r_list_data = None
    page = p_page
    paginator = Paginator(p_sensiList, NUM_DATA_PER_PAGE)
    try:
        r_list_data = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page=1
        r_list_data = paginator.page(page)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        r_list_data = paginator.page(paginator.num_pages)
    
    # 优化展示方式
    if(int(page)>5):
        r_pages_to_show=[i for i in paginator.page_range][int(page)-5:int(page)+5]
    else:
        r_pages_to_show=[i for i in paginator.page_range][:10]

    return r_list_data, r_pages_to_show


# 获取所有敏感信息详情列表, 对应：/sensi_details/get_list/
@csrf_exempt
@is_login
def get_list(request):
    list_data = None
    pages_to_show = None
    page = request.GET.get('page')     # page参数
    stat = request.GET.get('stat')   # stat参数
    
    sensiList_all = models.SensiDetails.objects.all().order_by("id")  # 给出所有记录中的数据
    amount_all = str(len(sensiList_all))
    print("敏感信息总数：" + amount_all)
    list_data, pages_to_show = render_resp(sensiList_all, page)
    
    if stat == 'all':
        return render(request,'sensi_list.html',{"list_data":list_data, "pages_to_show":pages_to_show, "amount":amount_all})
    elif stat == 'undone':
        sensiList_undone = models.SensiDetails.objects.all().filter(status=1).order_by("id")  # 只给出"未处理:1"的数据
        amount_undone = str(len(sensiList_undone))
        print("敏感信息未处理数: "+ amount_undone)
        list_data, pages_to_show = render_resp(sensiList_undone, page)
        return render(request,'sensi_list.html',{"list_data":list_data, "pages_to_show":pages_to_show, "amount":amount_undone})
    
    #  如果都不是，则直接返回所有
    return render(request,'sensi_list.html',{"list_data":list_data, "pages_to_show":pages_to_show, "amount":amount_all})


# 对应：/sensi_details/update/
@csrf_exempt
@is_login
def update(request):
    try:
        wiki = Wiki()
        result = wiki.get_page()
        details = []
        # 每次更新，根据爬取的url判断数据库中是否存在，不存在则插入defaults; 存在则不做啥
        for i in result:
            obj, created = models.SensiDetails.objects.get_or_create(url=i[1], 
                    defaults= {'status': 1, 'title': i[0], 'url': i[1], 'details': i[2]})
        
        result_undone = models.SensiDetails.objects.all().filter(status=1).order_by("id")  # 只给出"未处理:1"的数据, django.db.models.query.QuerySet类型
        send_mail(result_undone)  # 发送邮件(未处理的)
        return HttpResponse('success')
    except Exception:
        print(traceback.format_exc())
        return HttpResponse('fail')


@csrf_exempt
@is_login
def ignore(request):    # 2: 忽略
    url = request.POST.get("url")
    try:
        models.SensiDetails.objects.filter(url=url).update(status=2)
        return HttpResponse('success')
    except Exception:
        print(traceback.format_exc())
        return HttpResponse('fail')


@csrf_exempt
@is_login
def processed(request):  # 0: 已处理
    url = request.POST.get("url")
    try:
        models.SensiDetails.objects.filter(url=url).update(status=0)
        return HttpResponse('success')
    except Exception:
        print(traceback.format_exc())
        return HttpResponse('fail')


@csrf_exempt
@is_login
def undone(request):    # 1: 未处理
    url = request.POST.get("url")
    try:
        models.SensiDetails.objects.filter(url=url).update(status=1)    
        return HttpResponse('success')
    except Exception:
        print(traceback.format_exc())
        return HttpResponse('fail')
