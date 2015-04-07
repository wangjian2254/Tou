# coding=utf-8
# Date: 15/4/7'
# Email: wangjian2254@icloud.com
__author__ = u'王健'

from django import forms


class MovieForm(forms.Form):
    movie = forms.FileField()