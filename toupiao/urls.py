#coding=utf-8
'''
Created on 2011-3-19

@author: 王健
'''
from django.conf.urls import patterns
from toupiao.views import top, menu, welcome, savesubjectoption, showsubjectoption, showTouPiao, toupiaoPage, toupiaoResult, endnewslist,toupiaoerror, repassword, toupiaoExcel, initUser, \
    initUserPassword, showsubjectjoins, uploadsubjectjoins, deletesubjectjoins


urlpatterns = patterns('^toupiao/$',
                       (r'^top/$', top),
                       (r'^menu/$', menu),
                       (r'^welcome/$', welcome),
                       (r'^savesubjectoption/$', savesubjectoption),
                       (r'^showsubjectoption/$', showsubjectoption),
                       (r'^showsubjectjoins/$', showsubjectjoins),
                       (r'^uploadsubjectjoins/$', uploadsubjectjoins),
                       (r'^deletesubjectjoins/$', deletesubjectjoins),
                       (r'^showTouPiao/$', showTouPiao),
                       (r'^toupiaoPage/$', toupiaoPage),
                       (r'^toupiaoResult/$', toupiaoResult),
                       (r'^endnewslist/$', endnewslist),
                       (r'^error/$', toupiaoerror),
                       (r'^repassword/$', repassword),
                       (r'^toupiaoExcel/$', toupiaoExcel),
                       (r'^initUser/$', initUser),
                       (r'^initUserPassword/$', initUserPassword),



                       )