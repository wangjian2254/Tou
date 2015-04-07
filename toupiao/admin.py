# coding=utf-8
#author:u'王健'
#Date: 13-7-19
#Time: 下午9:01
from django.contrib.auth import get_user_model
from django.core import serializers
from django.forms import CheckboxSelectMultiple, Select
from django.forms.util import ErrorList
from django.http import HttpResponse
from toupiao.models import Subject, Option, Depatement

__author__ = u'王健'

from django.contrib import admin
from django.db import models
from django import forms


class OptionInline(admin.TabularInline):
    model = Option
    extra = 5


class SubjectForm(forms.ModelForm):
    userlist = get_user_model().objects.filter(is_staff=False).filter(is_active=True)
    joins = forms.ModelMultipleChoiceField(queryset=userlist, required=False, widget=CheckboxSelectMultiple,
                                           label=u'投票范围', validators=[])

    def clean(self):
        isuser = self.cleaned_data.get('isUser', None)
        # if isuser:
        #     joins = self.cleaned_data.get('joins', None)
        #     if len(joins) == 0:
        #         self._errors['joins'] = ErrorList([u'请选择投票范围'])
        return self.cleaned_data

    class Meta:
        model = Subject


class SubjectAdmin(admin.ModelAdmin):
    fields = ['title', 'content', 'single', 'num', 'startDate', 'endDate', 'isPub', 'isNoName', 'isReplay', 'isUser',
              'joins']
    list_display = ('title', 'startDate', 'endDate', 'isPub', 'isNoName', 'was_published_recently')
    list_filter = ('isPub', 'isNoName', 'startDate', 'endDate')
    search_fields = ('title',)
    ordering = ('-endDate',)
    inlines = (OptionInline,)

    actions = ['make_published']

    def make_published(self, request, queryset):
        rows_updated = queryset.update(isPub=True)
        if rows_updated == 1:
            message_bit = u"%s 条投票成功被设为公开状态。" % rows_updated
        self.message_user(request, message_bit)

    make_published.short_description = u"将所选的投票项目设为公开状态"

    form = SubjectForm


class OptionAdmin(admin.ModelAdmin):
    list_display = ('content', 'subject')
    list_filter = ('subject',)
    search_fields = ('subject__title',)
    ordering = ('subject', 'id')


class PersonAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'depate')
    list_filter = ('depate',)
    search_fields = ('first_name', 'username')
    ordering = ( 'id',)


admin.site.register(Subject, SubjectAdmin)
admin.site.register(Depatement)
admin.site.register(get_user_model(), PersonAdmin)
# admin.site.register(Option,OptionAdmin)

# admin.site.register(Product,ProductAdmin)



  