from django.contrib import admin
from .models import Genre, People, Movie, Onscreen


class GenreModelAdmin(admin.ModelAdmin):
    list_display = 'id', 'name'


class PeopleModelAdmin(admin.ModelAdmin):
    list_display = 'id', 'name'


class MovieModelAdmin(admin.ModelAdmin):
    list_display = 'id', 'name'


class OnscreenModelAdmin(admin.ModelAdmin):
    list_display = 'id',


admin.site.register(Genre, GenreModelAdmin)
admin.site.register(Movie, MovieModelAdmin)
admin.site.register(People, PeopleModelAdmin)
admin.site.register(Onscreen, OnscreenModelAdmin)
