# -*- coding: utf-8 -*-
# @Time    : 2020/4/6 19:51
# @Author  : Mr.Robot
# @Site    : 
# @File    : urls.py
# @Software: PyCharm

from django.urls import path, re_path
from RetrievalCore import views

urlpatterns = [
    re_path('^$', views.DocumentListView.as_view(), name="document_list"),
    re_path(r'^detail/(?P<document_id>\d+)/$', views.DocumentDetailView.as_view(), name="document_detail")
]

app_name = 'RetrievalCore'
