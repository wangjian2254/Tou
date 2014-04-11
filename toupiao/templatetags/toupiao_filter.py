#coding=utf-8
import urllib

__author__ = '王健'

from django import template
register=template.Library()

@register.filter(name='erweima')
def erweima(adminform,object_name):
    flag=True
    s=u"{"
    for fieldset in adminform:
        for line in fieldset:
            for field in line:
                if   field.field.name=='flag':
                    s+=u'"%s":"%s",'%(field.field.name,field.field.value())
                    if field.field.value():
                        flag=False
                elif  object_name=='ProductModel' and  field.field.name=='name':
                    try:
                        s+=u'"%s":"%s",'%(field.field.name,adminform.form.instance)
                        if field.field.value():
                            flag=False
                    except:
                        pass
                elif field.field.name=='':
                    s+=u'"%s":"%s",'%(field.field.name,field.field.value())
                    if field.field.value():
                        flag=False
    s+=u'"class":"%s"}'%object_name
    if not flag:
        return u'''<a href="http://qr.liantu.com/api.php?text=%s"><img src="http://qr.liantu.com/api.php?text=%s" border="0"/></a>'''%(urllib.quote(s.encode('utf-8')),urllib.quote(s.encode('utf-8')))
    return u'保存后才可以生成二维码'



@register.inclusion_tag('admin/toupiao/Subject/submit_line.html', takes_context=True)
def submit_row_option(context):
    """
    Displays the row of buttons for delete and save.
    """
    opts = context['opts']
    change = context['change']
    is_popup = context['is_popup']
    save_as = context['save_as']
    obj_id=''
    if context.has_key('object_id'):
        obj_id=context['object_id']
    return {
        'onclick_attrib': (opts.get_ordered_objects() and change
                            and 'onclick="submitOrderForm();"' or ''),
        'show_delete_link': (not is_popup and context['has_delete_permission']
                              and (change or context['show_delete'])),
        'show_save_as_new': not is_popup and change and save_as,
        'show_save_and_add_another': context['has_add_permission'] and
                            not is_popup and (not save_as or context['add']),
        'show_save_and_continue': not is_popup and context['has_change_permission'],
        'is_popup': is_popup,
        'show_save': True,
        'obj_id':obj_id,
        'show_save_option':context.has_key('object_id')

    }
