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
from toupiao.models import Depatement
from toupiao.tools import permission_required
from yzxweb.models import Movie, CodeChecker, CodeCheckRecord


def home(request):
    start = request.REQUEST.get('start', 1)
    start = int(start)
    list = Movie.objects.filter(is_active=True).order_by('-create_time')
    page = Paginator(list, 20)
    currentpage = page.page(start)
    return render_to_response('home.html', RequestContext(request, {'start': start, 'page': page, 'currentpage': currentpage}))


def show_movie(request):
    m = request.REQUEST.get('m')
    movie = Movie.objects.get(pk=m)
    html = 'movie.html'
    filetype = movie.movie.path.split('.')[-1].lower()
    if filetype in ['flv', 'mp4', 'mp3']:
        html = 'movie_flv.html'


    return render_to_response(html, RequestContext(request, {'movie': movie}))


@permission_required
def list_code_checker(request):
    dev_department = Depatement.objects.get(flag='dev')
    userlist = get_user_model().objects.filter(depate=dev_department, is_active=True)
    return render_to_response('update_code_checker.html', RequestContext(request, {'userlist': userlist}))


@permission_required
def update_code_checker(request):
    dev_department = Depatement.objects.get(flag='dev')
    userlist = get_user_model().objects.filter(depate=dev_department, is_active=True)
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
    userlist = get_user_model().objects.filter(depate=dev_department, is_active=True)
    return render_to_response('update_code_checker.html', RequestContext(request, {'userlist': userlist}))


@login_required
def update_code(request):

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
