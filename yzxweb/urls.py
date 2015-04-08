#coding=utf-8
'''
Created on 2011-3-19

@author: 王健
'''
from django.conf.urls import patterns
from yzxweb.views import update_code_checker, list_code_checker, update_code, list_movie, add_movie, del_movie, \
    update_log, update_pre_log, show_pre_log_list

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

                       (r'^update_log/$', update_log),
                       (r'^update_pre_log/$', update_pre_log),
                       (r'^show_pre_log_list/$', show_pre_log_list),



                       )