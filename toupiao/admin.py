#coding=utf-8
#author:u'王健'
#Date: 13-7-19
#Time: 下午9:01
from django.contrib.auth.models import User
from django.core import serializers
from django.forms import CheckboxSelectMultiple,Select
from django.forms.util import ErrorList
from django.http import HttpResponse
from toupiao.models import Subject, Option, Person, Depatement

__author__ = u'王健'

from django.contrib import admin
from django.db import models
from django import forms


class OptionInline(admin.TabularInline):
    model = Option
    extra = 5


class SubjectForm(forms.ModelForm):
    users = User.objects.filter(is_staff=False).filter(is_active=True)
    userlist = Person.objects.filter(user__in=users)
    joins = forms.ModelMultipleChoiceField(queryset=userlist, required=False, widget=CheckboxSelectMultiple,
                                           label=u'投票范围', validators=[])

    def clean(self):
        isuser = self.cleaned_data.get('isUser', None)
        if isuser:
            joins = self.cleaned_data.get('joins', None)
            if len(joins) == 0:
                self._errors['joins'] = ErrorList([u'请选择投票范围'])
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


class PersonForm(forms.ModelForm):
    psersons=[]
    for p in Person.objects.all():
        psersons.append(p.user_id)
    users = User.objects.exclude(pk__in=psersons).filter(is_active=True)
    user = forms.ModelChoiceField(queryset=users,required=True,widget=Select,label=u'账户')
        # .ModelMultipleChoiceField(queryset=userlist, required=False, widget=CheckboxSelectMultiple,
        #                                    label=u'投票范围', validators=[])

    # def clean(self):
    #     isuser = self.cleaned_data.get('isUser', None)
    #     if isuser:
    #         joins = self.cleaned_data.get('joins', None)
    #         if len(joins) == 0:
    #             self._errors['joins'] = ErrorList([u'请选择投票范围'])
    #     return self.cleaned_data

    class Meta:
        model = Person

class PersonAdmin(admin.ModelAdmin):
    list_display = ('truename', 'depate','user')
    list_filter = ('depate',)
    search_fields = ('truename','user__username')
    ordering = ( 'id',)
    form = PersonForm


admin.site.register(Subject, SubjectAdmin)
admin.site.register(Depatement)
admin.site.register(Person,PersonAdmin)
# admin.site.register(Option,OptionAdmin)

# admin.site.register(Product,ProductAdmin)



  