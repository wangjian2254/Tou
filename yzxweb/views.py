import datetime
from django.contrib.auth.models import AnonymousUser
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response

# Create your views here.
from django.template import RequestContext
from yzxweb.models import Movie


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


