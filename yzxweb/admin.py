from django.contrib import admin

# Register your models here.
from yzxweb.models import Movie


class MovieManage(admin.ModelAdmin):
    list_display = ('name', 'create_time')


admin.site.register(Movie, MovieManage)