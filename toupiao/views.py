#coding=utf-8
# Create your views here.
import json
import datetime
import uuid
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from Tou.settings import MEDIA_ROOT
from toupiao.tools import permission_required
from django.contrib.auth.models import AnonymousUser, User
from django.core.paginator import Paginator
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from toupiao.models import Subject, Option, Replay, Toupiao, Department, Person


@permission_required
def default2(request):
    return render_to_response('workframe.html', RequestContext(request))


@permission_required
def top(request):
    return render_to_response('topnav.html', RequestContext(request))


@permission_required
def menu(request):
    return render_to_response('menu.html', RequestContext(request))


@permission_required
def welcome(request):
    return render_to_response('welcome.html', RequestContext(request, {'num': range(30)}))


def redirectPage(request):
    if isinstance(request.user, AnonymousUser):
        return HttpResponseRedirect('/accounts/login/')
    if request.user.check_password('111111'):
        return HttpResponseRedirect('/toupiao/repassword/')

    if request.user.is_staff:
        return HttpResponseRedirect('/adminlogin/')
    else:
        return HttpResponseRedirect('/')


@login_required
def repassword(request):
    if request.method.lower() == 'get'.lower():
        return render_to_response('repassword.html',
                                  RequestContext(request, {'errors': False, 'username': request.user.username}))
    oldpassword = request.POST.get('oldpassword', '')
    newpassword = request.POST.get('newpassword', '')
    newrepassword = request.POST.get('renewpassword', '')

    if not oldpassword or not newpassword or not newrepassword:
        return render_to_response('repassword.html',
                                  RequestContext(request, {'errors': True, 'username': request.user.username}))
    if request.user.check_password(oldpassword):
        if newpassword == newrepassword:
            request.user.set_password(newpassword)
            request.user.save()
            return HttpResponseRedirect('/accounts/profile/')
    else:
        return render_to_response('repassword.html',
                                  RequestContext(request, {'errors': True, 'username': request.user.username}))


@permission_required
def showsubjectoption(request):
    subjectid = request.GET.get('subjectid')
    subject = Subject.objects.get(pk=subjectid)
    options = Option.objects.filter(subject=subject).order_by('id')
    return render_to_response('admin/toupiao/subjectoptions.html', RequestContext(request, {'newitems': range(10),
                                                                                            'options': options,
                                                                                            'oldcount': options.count(),
                                                                                          'subject': subject}))
@permission_required
def showsubjectjoins(request):
    subjectid = request.REQUEST.get('subjectid')
    subject = Subject.objects.get(pk=subjectid)
    joins = subject.joins.all()
    users = []
    d = {}
    for u in joins.order_by('depate'):
        if d.has_key(unicode(u.depate)):
            users.append((False,False,u))
        else:
            users.append((unicode(u.depate),joins.filter(depate=u.depate).count(),u))
        d[unicode(u.depate)] = True

    return render_to_response('admin/toupiao/subjectjoins.html', RequestContext(request, {'joins': users,
                                                                                  'subject': subject,"msg":request.REQUEST.get("msg",""),"result":request.REQUEST.get("result","")}))

@permission_required
def deletesubjectjoins(request):
    sid = request.REQUEST.get("subjectid")
    pid = request.REQUEST.get("pid")
    if sid and pid:
        subject = Subject.objects.get(pk=sid)
        person = Person.objects.get(pk=pid)
        subject.joins.remove(person)
        return HttpResponseRedirect('/toupiao/showsubjectjoins/?subjectid=%s&result=%s&msg=%s'%(sid,"succeed",u"移除 %s 成功。"%person.truename))
    else:
        return HttpResponseRedirect('/toupiao/showsubjectjoins/?subjectid=%s&result=%s&msg=%s'%(sid,"warning",u"操作失败"))



@permission_required
def uploadsubjectjoins(request):
    sid = request.REQUEST.get("subjectid")
    if not request.FILES.has_key('excel'):
        return HttpResponseRedirect('/toupiao/showsubjectjoins/?subjectid=%s&result=%s&msg=%s'%(sid,"warning",u"请上传Excel文件，格式为2003版。"))

    f=request.FILES["excel"]

    if f.name.lower().find('.xls')<0:
        return HttpResponseRedirect('/toupiao/showsubjectjoins/?subjectid=%s&result=%s&msg=%s'%(sid,"warning",u"请上传Excel文件，格式为2003版。"))
    fpath= MEDIA_ROOT+'upload/'+str(uuid.uuid4())+'.xls'
    try:
        fileatt=open(fpath,'wb+')
        for chunk in f.chunks():
            fileatt.write(chunk)
        fileatt.close()
        # from xpinyin import Pinyin
        import xlrd
        # p=Pinyin()

        book = xlrd.open_workbook(fpath)
        sheet=book.sheet_by_name(book.sheet_names()[0])
        rownum=sheet.nrows
        depatedict={}
        emptyusers=[]
        depate = None
        truenamedict = {}
        for i in range(1,rownum):
            row_data = sheet.row_values(i,0,2)
            if row_data[0]:
                depate = row_data[0].strip().split('\n')[0].split('\r')[0]
            nickname = row_data[1].strip()
            if truenamedict.has_key(nickname):
                return  HttpResponseRedirect('/toupiao/showsubjectjoins/?subjectid=%s&result=%s&msg=%s'%(sid,"warning",u"文件中有重复的姓名：%s"%nickname))

            truenamedict[nickname]=True
            if depate:
                if not depatedict.has_key(depate):
                    depatedict[depate] = []
                depatedict[depate].append(nickname)
            else:
                emptyusers.append(nickname)
        subject = Subject.objects.get(pk=sid)
        subject.joins.clear()
        for n in emptyusers:
            u,c = User.objects.get_or_create(username=n)
            if c:
                u.set_password('111111')
                u.save()
                p = Person()
                p.user = u
            else:
                p = u.person
            if not p:
                p = Person()
                p.user = u
            p.truename = n
            p.save()
            subject.joins.add(p)
        for d,ns in depatedict.items():
            dep,c = Department.objects.get_or_create(name=d)
            if c:
                dep.save()
            for n in ns:
                u,c = User.objects.get_or_create(username=n)
                if c:
                    u.set_password('111111')
                    u.save()
                    p = Person()
                    p.user = u
                else:
                    p = u.person
                if not p:
                    p = Person()
                    p.user = u
                p.truename = n
                p.depart = dep
                p.save()
                subject.joins.add(p)
        return HttpResponseRedirect('/toupiao/showsubjectjoins/?subjectid=%s&result=%s&msg=%s'%(sid,"succeed",u"导入成功"))
    except Exception,e:
            import os
            if  os.path.isfile(fpath):
                os.remove(fpath)
            raise e
    else:
        import os
        if  os.path.isfile(fpath):
            os.remove(fpath)


@permission_required
def savesubjectoption(request):
    subjectid = request.POST.get('subjectid', '')
    if not subjectid:
        raise Http404()
    subject = Subject.objects.get(pk=subjectid)
    selectoptionid = request.POST.getlist('selectoption')
    Option.objects.filter(subject=subject).exclude(pk__in=selectoptionid).delete()
    for i in selectoptionid:
        oldoption = Option.objects.get(pk=i)
        oldoption.content = request.POST.get('option%s' % i, '')
        oldoption.save()
    for i in range(1, 12):
        content = request.POST.get('newoption%s' % i, '')
        if content:
            newoption = Option()
            newoption.subject = subject
            newoption.content = request.POST.get('newoption%s' % i, '')
            newoption.save()
    return HttpResponseRedirect('/toupiao/showsubjectoption/?subjectid=%s' % subjectid)


def showTouPiao(request):
    subjectid = request.GET.get('subjectid')
    subject = Subject.objects.get(pk=subjectid)
    options = Option.objects.filter(subject=subject).order_by('id')
    needTou=True
    if not subject.isNoName and request.user.is_anonymous():
        needTou=False
    elif subject.isUser and subject.joins.filter(user=request.user).count()==0:
        needTou=False

    return render_to_response('jianlilook.html', RequestContext(request, {'obj': subject, 'objtype': 'subject','needTou':needTou,
                                                                          'options': options, 'subject': subject}))


def toupiaoerror(request):
    type = request.REQUEST.get('type', 'error')
    subjectid = request.REQUEST.get('subjectid')
    if subjectid:
        subject = Subject.objects.get(pk=subjectid)
        return render_to_response('toupiaoerror.html', RequestContext(request, {'subject': subject, 'type': type}))
    else:
        subject={}
        return render_to_response('toupiaoerror2.html', RequestContext(request, {'subject': subject, 'type': type}))



def toupiaoPage(request):
    subjectid = request.REQUEST.get('subjectid')
    subject = Subject.objects.get(pk=subjectid)
    selectoption = request.REQUEST.getlist('selectoption')
    if subject.single:
        if len(selectoption) > 1 or len(selectoption)==0:
            return HttpResponseRedirect('/toupiao/error/?type=error&subjectid=%s' % subjectid)
    else:
        if len(selectoption) > subject.num or len(selectoption)==0:
            return HttpResponseRedirect('/toupiao/error/?type=duoerror&subjectid=%s' % subjectid)
    if not subject.isNoName and isinstance(request.user, AnonymousUser):
        return HttpResponseRedirect('/toupiao/error/?type=erroruser&subjectid=%s' % subjectid)

    if not subject.isNoName and subject.isUser and subject.joins.filter(user=request.user).count()==0:
        return HttpResponseRedirect('/toupiao/error/?type=wuquanxian&subjectid=%s' % subjectid)

    if request.session.has_key('subjectlist') and subjectid in request.session['subjectlist']:
        return HttpResponseRedirect('/toupiao/error/?type=chongfu&subjectid=%s' % subjectid)
    if subject.startDate > timezone.now() or subject.endDate < timezone.now():
        return HttpResponseRedirect('/toupiao/error/?type=dateout&subjectid=%s' % subjectid)
    if not request.session.has_key('subjectlist'):
        request.session['subjectlist'] = []
        sessionset = []
    else:
        sessionset = request.session['subjectlist']
    optionslist = Option.objects.filter(pk__in=selectoption)
    toupiao = Toupiao()

    if not subject.isNoName and not isinstance(request.user, AnonymousUser):
        toupiao.user = request.user
    if not isinstance(request.user, AnonymousUser):
        if 0<Toupiao.objects.filter(subject=subject).filter(user=request.user).count():
            return HttpResponseRedirect('/toupiao/error/?type=chongfu&subjectid=%s' % subjectid)
    toupiao.subject = subject
    toupiao.dateTime = timezone.now()
    toupiao.save()
    for opt in optionslist:
        toupiao.options.add(opt)
    toupiao.save()
    sessionset.append(subjectid)
    request.session['subjectlist'] = sessionset
    return render_to_response('toupiaosuccess.html', RequestContext(request, {'subject': subject}))


def toupiaoResult(request):
    subjectid = request.REQUEST.get('subjectid')
    subject = Subject.objects.get(pk=subjectid)
    optdict = {}
    totalnum = 0
    for toupiao in Toupiao.objects.filter(subject=subject):
        for opt in toupiao.options.all():
            if not optdict.has_key(str(opt.pk)):
                optdict[str(opt.pk)] = 0
            optdict[str(opt.pk)] += 1
            totalnum += 1
    optionlist = []
    for opt in Option.objects.filter(subject=subject).order_by('id'):
        if optdict.has_key(str(opt.pk)):
            optionlist.append({'option': opt, 'num': optdict[str(opt.pk)]})
        else:
            optionlist.append({'option': opt, 'num': 0})

    return render_to_response('toupiaoresult.html', RequestContext(request, {'obj': subject, 'objtype': 'subjectresult',
                                                                             'subject': subject,
                                                                             'optionlist': optionlist,
                                                                             'total': totalnum}))

@permission_required
def initUser(request):
    import json,os
    userlist=json.load(open(os.path.join(os.path.dirname(__file__), '../Tou/').replace('\\','/')+'user.json'))
    bmdict={}
    for u in userlist:
        if not bmdict.has_key(u['bm']):
            bm=Department()
            bm.name=u['bm']
            bm.save()
            bmdict[u['bm']]=bm

        user=User()
        user.username=u['username']
        user.set_password('111111')
        user.is_active=True
        user.is_staff=False
        user.is_superuser=False
        user.save()
        person=Person()
        person.depart=bmdict[u['bm']]
        person.user=user
        person.truename=u['truename']
        person.save()
    return HttpResponse(u'导入成功')
@permission_required
def toupiaoExcel(request):
    subjectid = request.REQUEST.get('subjectid')
    optionid = request.REQUEST.get('optionid')
    subject = Subject.objects.get(pk=subjectid)
    if subject.isNoName:
        return HttpResponse(u'匿名投票不可导出')
    filename=u'%s'%subject.title
    if optionid:
        option = Option.objects.get(pk=optionid)
        if option.subject.pk!=subject.pk:
            raise Http404
        filename+=u'——%s'%option.content

    response = HttpResponse(mimetype=u'application/ms-excel')
    filenames = u'%s.xls'%filename
    response['Content-Disposition'] = (u'attachment;filename=%s' % filenames).encode('utf-8')
    import xlwt
    from xlwt import Font, Alignment

    style1 = xlwt.XFStyle()
    font1 = Font()
    font1.height = 260
    font1.name = u'仿宋'
    style1.font = font1
    algn = Alignment()
    algn.horz = Alignment.HORZ_LEFT
    style1.alignment = algn
    style1.font = font1
    style0 = xlwt.XFStyle()
    algn0 = Alignment()
    algn0.horz = Alignment.HORZ_CENTER
    font = Font()
    font.height = 220
    font.bold = False
    font.name = u'仿宋'
    style0.alignment = algn0
    style0.font = font
    wb = xlwt.Workbook()
    ws = wb.add_sheet(u"人员名单", cell_overwrite_ok=True)
    ws.header_str = filename
    ws.footer_str =''
    rownum = 0
    num=1
    query=Toupiao.objects.filter(subject=subject)
    if optionid:
        query=query.filter(options=option)
        ws.write_merge(rownum,rownum,0,0,u'序号',style0)
        ws.write_merge(rownum,rownum,1,1,u'部门',style0)
        ws.write_merge(rownum,rownum,2,2,u'人员',style0)
        rownum+=1
        for toupiao in query:
            ws.write_merge(rownum,rownum,0,0,num,style0)
            ws.write_merge(rownum,rownum,1,1,unicode(getattr(toupiao.user.person,'depate',u'无')),style0)
            ws.write_merge(rownum,rownum,2,2,toupiao.user.person.truename,style0)
            rownum+=1
            num+=1
    else:
        for opt in Option.objects.filter(subject=subject):
            ws.write_merge(rownum,rownum,0,2,u'选项：%s'%opt.content,style1)
            rownum+=1
            ws.write_merge(rownum,rownum,0,0,u'序号',style0)
            ws.write_merge(rownum,rownum,1,1,u'部门',style0)
            ws.write_merge(rownum,rownum,2,2,u'人员',style0)
            rownum+=1
            for toupiao in query.filter(options=opt):
                ws.write_merge(rownum,rownum,0,0,num,style0)
                ws.write_merge(rownum,rownum,1,1,unicode(getattr(toupiao.user.person,'depate',u'无')),style0)
                ws.write_merge(rownum,rownum,2,2,toupiao.user.person.truename,style0)
                rownum+=1
                num+=1
    width=256*10
    ws.col(0).width = width
    ws.col(1).width = width*3
    ws.col(2).width = width*2
    wb.save(response)
    return response

def newslist(request):
    '''
    栏目下新闻列表
    '''
    start = request.REQUEST.get('start', 1)
    start = int(start)
    list = Subject.objects.filter(endDate__gte=timezone.now()).filter(isPub=True)
    page = Paginator(list, 20)
    currentpage = page.page(start)
    return render_to_response('toupiaolist.html',
                              RequestContext(request, {'start': start, 'page': page, 'currentpage': currentpage}))


def endnewslist(request):
    '''
    栏目下新闻列表
    '''
    start = request.REQUEST.get('start', 1)
    start = int(start)
    list = Subject.objects.filter(endDate__lte=timezone.now()).filter(isPub=True)
    page = Paginator(list, 20)
    currentpage = page.page(start)
    return render_to_response('toupiaolistend.html',
                              RequestContext(request, {'start': start, 'page': page, 'currentpage': currentpage}))


def commentAdd(request):
    if hasattr(request, 'environ'):
        fromurl = request.environ.get('HTTP_REFERER', '/')
    if hasattr(request, 'META'):
        fromurl = request.META.get('HTTP_REFERER', '/')
    type = request.POST.get('type', '')
    content = request.POST.get('content', '')
    #    content=content.replace('<','&lt;')
    #    content=content.replace('>','&gt;')
    face = request.POST.get('face', '')
    pk = request.POST.get('pk', '')
    if pk and content and type:
        replay = Replay()
        if not isinstance(request.user, AnonymousUser):
            replay.user = request.user
        replay.objid = int(pk)
        if face:
            replay.face = int(face)
        replay.content = content
        replay.type = type
        replay.save()
    return HttpResponseRedirect(fromurl)


@csrf_exempt
def replay(request):
    objid = request.POST.get('pk', '')
    type = request.POST.get('type', '')
    replaynum = Replay.objects.filter(objid=int(objid)).filter(type=type).count()
    return HttpResponse('{"success":true,"replaynum":%s}' % replaynum)


@csrf_exempt
def commentList(request):
    type = request.POST.get('type', '')
    objid = request.POST.get('pk', '')
    replaylist = []
    for replay in Replay.objects.filter(type=type).filter(objid=objid).order_by('-updatetime')[:40]:
        rmap = {}
        rmap['id'] = replay.pk
        rmap['face'] = replay.face
        rmap['content'] = replay.content
        rmap['createDate'] = replay.updatetime.strftime('%Y年%m月%d日 %H:%M:%S')
        rmap['fatherid'] = replay.father_id
        if replay.user:
            rmap['userid'] = replay.user.pk
            rmap['username'] = replay.user.username
            rmap['first_name'] = replay.user.first_name
        else:
            rmap['userid'] = 0
            rmap['username'] = u'匿名用户'
            rmap['first_name'] = replay.user.first_name

        replaylist.append(rmap)
    html = json.dumps(replaylist)
    return HttpResponse(html)



@permission_required
def initUserPassword(request):

    for user in User.objects.all():
        user.set_password('111111')
        user.save()

    return HttpResponse(u'全部用户的密码都改为了：111111')