#coding=utf-8
from datetime import datetime
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils import timezone


class Movie(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'影片名称')
    desc = models.TextField(verbose_name=u'描述')
    create_time = models.DateTimeField(default=timezone.now, verbose_name=u'创建时间')
    movie = models.FileField(verbose_name=u'视频文件', upload_to='movie/', )
    is_active = models.BooleanField(default=True, verbose_name=u'是否可用')
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.name


class CodeChecker(models.Model):
    """
    代码走查者
    by:王健 at:2015-4-6
    """
    user = models.ForeignKey(User, verbose_name=u'打分者', related_name='dafen_user_checker')
    to_user = models.ForeignKey(User, verbose_name=u'被打分者', related_name='beidafen_user_checker')
    is_active = models.BooleanField(default=True, verbose_name=u'是否走查')


class CodeCheckRecord(models.Model):
    """
    代码走查
    by:王健 at:2015-4-6
    """
    user = models.ForeignKey(User, verbose_name=u'打分者', related_name='dafen_user')
    to_user = models.ForeignKey(User, verbose_name=u'被打分者', related_name='beidafen_user')
    date = models.DateField(default=timezone.now, verbose_name=u'日期')
    num = models.IntegerField(default=0, verbose_name=u'打分值')

    class Meta():
        unique_together = (('user', 'to_user', 'date'),)


class WorkLog(models.Model):
    """
    工作日志
    by:王健 at:2015-4-6
    """
    user = models.ForeignKey(User, verbose_name=u'工作者')
    date = models.DateField(default=timezone.now, verbose_name=u'日期')
    content = models.CharField(max_length=100, verbose_name=u'计划内容')
    num = models.IntegerField(default=3, verbose_name=u'评价打分')
    replay = models.CharField(max_length=100, verbose_name=u'评价')
    is_weekly = models.BooleanField(default=False, verbose_name=u'是否周工作日志')


class WorkLogRecord(models.Model):
    """
    工作日志记录
    by:王健 at:2015-4-6
    """
    worklog = models.ForeignKey(WorkLog, verbose_name=u'工作日志')


    sort = models.IntegerField(default=0, verbose_name=u'排序')