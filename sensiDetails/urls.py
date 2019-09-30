# coding=utf-8
from django.conf.urls import url, include
from django.contrib import admin

from sensiDetails import views as sensi_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^login/', sensi_views.auth,name='auth'),
    url(r'^$', sensi_views.index, name="index"),  # 首页
    

    # 敏感信息
    url(r'^sensi_details/get_list/$', sensi_views.get_list, name="sensi_details_list"),
    url(r'^sensi_details/update/$', sensi_views.update, name="sensi_details_update"),  # 抓取数据，更新
    # 处理方式
    url(r'^sensi_details/undone/$', sensi_views.undone, name="sensi_oper_undone"),            # 标记为：未处理
    url(r'^sensi_details/ignore/$', sensi_views.ignore, name="sensi_oper_ignore"),            # 标记为：忽略
    url(r'^sensi_details/processed/$', sensi_views.processed, name="sensi_oper_processed"),   # 标记为：已处理
    
]

