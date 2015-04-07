#coding=utf-8
'''
Created on 2011-3-19

@author: 王健
'''
from django.conf.urls import patterns
from yzxweb.views import update_code_checker, list_code_checker, update_code, list_movie, add_movie, del_movie

urlpatterns = patterns('^yzxweb/$',

                       # (r'^add_log/$', ''),
                       # (r'^list_log/$', ''),
                       (r'^list_code_checker/$', list_code_checker),
                       (r'^update_code_checker/$', update_code_checker),
                       (r'^list_code/$', update_code),
                       (r'^update_code/$', update_code),
                       (r'^list_movie/$', list_movie),
                       (r'^add_movie/$', add_movie),
                       (r'^del_movie/$', del_movie),



                       )