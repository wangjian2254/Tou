#coding=utf-8
import datetime
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response

# Create your views here.
from django.template import RequestContext
from django.utils import timezone
from toupiao.models import Department
from toupiao.tools import permission_required
from yzxweb.forms import MovieForm
from yzxweb.models import Movie, CodeChecker, CodeCheckRecord, WorkLogDate, WorkLogWeek


def home(request):
    """
    默认界面，显示视频列表
    by:王健 at:2015-4-7
    :param request:
    :return:
    """
    start = request.REQUEST.get('start', 1)
    start = int(start)
    list = Movie.objects.filter(is_active=True).order_by('-create_time')
    page = Paginator(list, 20)
    currentpage = page.page(start)
    return render_to_response('home.html', RequestContext(request, {'start': start, 'page': page, 'currentpage': currentpage}))


@permission_required
def list_movie(request):
    """
    视频管理 列表
    by:王健 at:2015-4-7
    :param request:
    :return:
    """
    start = request.REQUEST.get('start', 1)
    start = int(start)
    list = Movie.objects.filter(is_active=True).order_by('-create_time')
    page = Paginator(list, 20)
    currentpage = page.page(start)
    return render_to_response('movie_list.html', RequestContext(request, {'start': start, 'page': page, 'currentpage': currentpage}))


@permission_required
def del_movie(request):
    """
    视频删除
    by:王健 at:2015-4-7
    :param request:
    :return:
    """
    m = request.REQUEST.get('m')
    movie = Movie.objects.get(pk=m)
    movie.is_active = False
    movie.delete()
    return HttpResponseRedirect('/yzxmanage/list_movie/?start=%s' % request.REQUEST.get('start'))


@permission_required
def add_movie(request):
    """
    添加视频
    by:王健 at:2015-4-7
    :param request:
    :return:
    """
    if request.method == "POST":
        movie = Movie()
        movie.user = request.user
        movie.desc = request.REQUEST.get("desc", "")
        movie.name = request.REQUEST.get("name", timezone.now().strftime('%Y-%m-%d'))
        movie.is_active = True
        mf = MovieForm(request.POST, request.FILES)
        if mf.is_valid():
            movie.movie = mf.cleaned_data['movie']
        else:
            return render_to_response('add_movie.html', RequestContext(request, {'movie': movie}))
        movie.save()
        return HttpResponseRedirect('/yzxmanage/list_movie/')
    else:
        return render_to_response('add_movie.html', RequestContext(request, {'movie': {}}))


def show_movie(request):
    """
    显示视频
    by:王健 at:2015-4-7
    :param request:
    :return:
    """
    m = request.REQUEST.get('m')
    movie = Movie.objects.get(pk=m)
    html = 'movie.html'
    filetype = movie.movie.path.split('.')[-1].lower()
    if filetype in ['flv', 'mp4', 'mp3']:
        html = 'movie_flv.html'


    return render_to_response(html, RequestContext(request, {'movie': movie, 'obj': movie, 'objtype': 'movie'}))


@permission_required
def list_code_checker(request):
    """
    代码走查列表
    by:王健 at:2015-4-7
    :param request:
    :return:
    """
    dev_department = Department.objects.get(flag='dev')
    userlist = get_user_model().objects.filter(depart=dev_department, is_active=True)
    return render_to_response('update_code_checker.html', RequestContext(request, {'userlist': userlist}))


@permission_required
def update_code_checker(request):
    """
    代码走查 设置走查对象
    by:王健 at:2015-4-7
    :param request:
    :return:
    """
    dev_department = Department.objects.get(flag='dev')
    userlist = get_user_model().objects.filter(depart=dev_department, is_active=True)
    for user in userlist:
        userpk = request.REQUEST.getlist('%s' % user.pk)
        if userpk:
            user.dafen_user_checker.exclude(to_user_id__in=userpk).update(is_active=False)
            user.dafen_user_checker.filter(to_user_id__in=userpk).update(is_active=True)
            for u in userpk:
                if not user.dafen_user_checker.filter(to_user_id=u).exists():
                    cc = CodeChecker()
                    cc.user = user
                    cc.to_user_id = u
                    cc.is_active = True
                    cc.save()

        else:
            user.dafen_user_checker.all().update(is_active=False)
            # CodeChecker.objects.filter(user=user).
    userlist = get_user_model().objects.filter(depart=dev_department, is_active=True)
    return render_to_response('update_code_checker.html', RequestContext(request, {'userlist': userlist}))


@login_required
def update_code(request):
    """
    代码走查打分
    by:王健 at:2015-4-7
    :param request:
    :return:
    """
    today = timezone.now()
    for u in request.user.dafen_user_checker.filter(is_active=True):
        dafen = request.REQUEST.get('%s_num' % u.to_user_id)
        if dafen:
            code, created = CodeCheckRecord.objects.get_or_create(user=request.user, to_user_id=u.to_user_id, date=today)
            if created:
                code.num = int(dafen)
                code.save()
    userlist = request.user.dafen_user_checker.filter(is_active=True)
    l = []
    for u in userlist:
        code = CodeCheckRecord.objects.filter(user=request.user, to_user_id=u.to_user_id, date=today)[:1]
        if code:
            l.append({'pk': u.to_user_id, 'first_name': u.to_user.first_name, 'num': code[0].num})
        else:
            l.append({'pk': u.to_user_id, 'first_name': u.to_user.first_name, 'num': -1})
    week = today.weekday()+1
    if week == 1:
        day = u"一"
    elif week == 2:
        day = u'二'
    elif week == 3:
        day = u'三'
    elif week == 4:
        day = u'四'
    elif week == 5:
        day = u'五'
    elif week == 6:
        day = u'六'
    elif week == 7:
        day = u'日'
    return render_to_response('update_code.html', RequestContext(request, {'userlist': l, 'today': today.strftime('%Y-%m-%d'), 'day': day}))


@login_required
def update_date_log(request):
    """
    填写日志
    by:王健 at:2015-4-7
    :param request:
    :return:
    """
    today = timezone.now()
    if request.method == "POST":
        worklog, created = WorkLogDate.objects.get_or_create(user=request.user, date=today)
        worklog.content = request.REQUEST.get("content", "")
        worklog.save()
        result = {'msg': u'保存今日工作日志成功。', 'result': 'succeed'}
    else:
        worklog, created = WorkLogDate.objects.get_or_create(user=request.user, date=today)
        result = {}
    r = {'worklog': worklog, 'pre_worklog': WorkLogDate.objects.filter(date__gt=today)}
    r.update(result)
    return render_to_response('update_log.html', RequestContext(request, r))


@login_required
def list_log(request):
    """
    填写日志
    by:王健 at:2015-4-7
    :param request:
    :return:
    """
    date = request.REQUEST.get('date', '')
    if date:
        d = datetime.datetime.strptime(date, '%m/%d/%Y')
    else:
        d = timezone.now() + datetime.timedelta(days=-7)
    user_id = request.REQUEST.get('user_id', '')
    if not user_id:
        user_id = request.user.pk
    userobj = get_user_model().objects.get(pk=user_id)
    userlist = []
    # if request.user.pk == request.user.depart.leader_id:
    userlist = get_user_model().objects.filter(depart=request.user.depart).filter(is_active=True)
    userlist2 = get_user_model().objects.exclude(depart=request.user.depart).filter(is_active=True)

    r = {'date': d, 'user_id': int(user_id),
         'pre_worklog': WorkLogDate.objects.filter(date__gt=d, user_id=user_id)[:10], 'userlist': userlist,
         'userlist2': userlist2, 'userobj': userobj, 'obj': userobj, 'objtype': 'list_log'}
    return render_to_response('list_log.html', RequestContext(request, r))


@login_required
def update_week_log(request):
    """
    填写日志
    by:王健 at:2015-4-7
    :param request:
    :return:
    """
    today = timezone.now()
    if request.method == "POST":
        worklog, created = WorkLogWeek.objects.get_or_create(user=request.user, date=today)
        if not created:
            worklog.major_team.clear()
            worklog.minor_team.clear()
        worklog.content = request.REQUEST.get("content", "")
        worklog.major_team.clear()
        for u in get_user_model().objects.filter(pk__in=request.REQUEST.getlist('major')):
            worklog.major_team.add(u)
        worklog.minor_team.clear()
        for u in get_user_model().objects.filter(pk__in=request.REQUEST.getlist('minor')):
            worklog.minor_team.add(u)
        if request.REQUEST.get('leader'):
            worklog.leader = get_user_model().objects.get(pk=request.REQUEST.get('leader'))
        else:
            worklog.leader = None
        worklog.save()
        result = {'msg': u'保存今日工作日志成功。', 'result': 'succeed'}
    else:
        worklog, created = WorkLogWeek.objects.get_or_create(user=request.user, date=today)
        result = {}
    r ={'worklog': worklog, 'departmentlist': Department.objects.all(), 'department': request.user.depart, 'alluser': get_user_model().objects.filter(is_active=True)}
    r.update(result)
    return render_to_response('update_week_log.html', RequestContext(request, r))

@login_required
def update_pre_log(request):
    """
    填写 计划日志
    by:王健 at:2015-4-8
    :param request:
    :return:
    """
    today = timezone.now()
    wid = request.GET.get('w')
    date = request.REQUEST.get('date', '')
    if date:
        d = datetime.datetime.strptime(date, '%m/%d/%Y')
    if request.method == "GET":
        if wid:
            n_worklog = WorkLogDate.objects.get(pk=wid)
        if date:
            if today.strftime('%Y-%m-%d') < d.strftime('%Y-%m-%d') and (today + datetime.timedelta(days=11)).strftime('%Y-%m-%d') > d.strftime('%Y-%m-%d'):
                n_worklog, created = WorkLogDate.objects.get_or_create(user=request.user, date=d)
            else:
                return render_to_response('update_pre_log.html', RequestContext(request, {'msg': u'只能制定未来10天内的工作计划', 'result': 'warning'}))
        return render_to_response('update_pre_log.html', RequestContext(request, {'worklog': n_worklog}))
    else:

            if today.strftime('%Y-%m-%d') < d.strftime('%Y-%m-%d') and (today + datetime.timedelta(days=11)).strftime('%Y-%m-%d') > d.strftime('%Y-%m-%d'):
                n_worklog, created = WorkLogDate.objects.get_or_create(user=request.user, date=d)
                n_worklog.pre_content = request.REQUEST.get("pre_content", "")
                n_worklog.save()
                return render_to_response('update_pre_log.html', RequestContext(request, {'worklog': n_worklog, 'msg': u'指定工作计划成功。', 'result': 'succeed'}))
            else:
                return render_to_response('update_pre_log.html', RequestContext(request, {'msg': u'只能制定未来10天内的工作计划', 'result': 'warning'}))
    return render_to_response('update_pre_log.html', RequestContext(request, {'worklog': worklog}))


@login_required
def show_pre_log_list(request):
    """
    显示 计划日志列表
    by:王健 at:2015-4-7
    :param request:
    :return:
    """
    today = timezone.now()
    loglist = WorkLog.objects.filter(user=request.user, date__gt=today).order_by('id')
    return render_to_response('pro_log_list.html', RequestContext(request, {'loglist': loglist}))

