from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.auth.views import login, logout
from Tou import settings
from toupiao.views import default2, replay, commentAdd, commentList, newslist, redirectPage
from yzxweb.views import home, show_movie

admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'Tou.views.home', name='home'),
                       # url(r'^Tou/', include('Tou.foo.urls')),
                       (r'^$', home),
                       (r'^movie$', show_movie),
                       url(r'^newslist/$', newslist),
                       url(r'^adminlogin/$', default2),

                       url(r'^toupiao/', include('toupiao.urls')),
                       url(r'^ueditor/', include('ueditor.urls')),

                       (r'^accounts/login/$', login, {'template_name': 'login.html'}),
                       (r'^accounts/logout/$', logout, {'template_name': 'logout.html'}),
                       (r'^accounts/profile/$', redirectPage),
                       (r'^replay', replay),
                       (r'^commentAdd', commentAdd),
                       (r'^commentList', commentList),

                       url(r'^yzxmanage/', include('yzxweb.urls')),
                       url(r'^ueditor/', include('ueditor.urls')),
                       # (r'^admin/toupiao/subject/add/$', addSubject),
                       # Uncomment the admin/doc line below to enable admin documentation:
                       url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
                       # Uncomment the next line to enable the admin:
                       url(r'^admin/', include(admin.site.urls)),


)
