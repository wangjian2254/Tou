#coding=utf-8
#Date: 11-12-8
#Time: 下午10:28
from django.http import HttpResponseRedirect

__author__ = u'王健'

def permission_required(func=None):
    def test(request, *args, **kwargs):
        if request.user.is_staff and request.user.is_active:
            return func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/toupiao/error/?type=quanxian')
    return test