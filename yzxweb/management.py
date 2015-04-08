# coding=utf-8
# Date: 15/4/7'
# Email: wangjian2254@icloud.com
import sys
from django.db.models import signals
from django.contrib.auth import models as django_user, get_user_model
from toupiao.models import Department

__author__ = u'王健'
reload(sys)
sys.setdefaultencoding('utf8')
from xml.etree import ElementTree

def add_default_app(**kwargs):
    """
    初始化数据
    by:王健 at:2015-3-6
    :param kwargs:
    :return:
    """
    userxml = ElementTree.parse('users.xml')
    # 获取element的方法
    # 1 通过getiterator
    lst_node = userxml.getiterator("RTX_Dept")[0]
    depdict = {}
    for node in lst_node:
        dep, created = Department.objects.get_or_create(name=node.attrib['DeptName'])
        depdict[node.attrib['DeptID']] = dep
        if depdict.has_key(node.attrib['PDeptID']):
            dep.father = depdict[node.attrib['PDeptID']]
        dep.save()
        print node
    lst_node = userxml.getiterator("Sys_User")[0]
    userdict = {}
    for node in lst_node:
        user, created = get_user_model().objects.get_or_create(username=node.attrib['UserName'])
        if created:
            user.set_password('123456')
        if node.attrib['Gender'] == '0':
            user.male = False
        else:
            user.male = True
        user.first_name = node.attrib['Name']
        if node.attrib['Email']:
            user.email = node.attrib['Email']
        user.save()
        userdict[node.attrib['ID']] = user
        print node
    lst_node = userxml.getiterator("RTX_DeptUser")[0]
    for node in lst_node:
        userdict[node.attrib['UserID']].depart = depdict[node.attrib['DeptID']]
        userdict[node.attrib['UserID']].save()

        print node



signals.post_syncdb.connect(add_default_app, sender=django_user,dispatch_uid='yzxweb.create_defaultuser')
