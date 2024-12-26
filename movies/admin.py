from django.contrib import admin
from .models import Genre, MovieDirector, MovieGenre, Tag, Movie


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


class GenreInline(admin.TabularInline):
    model = MovieGenre


class DirectorInline(admin.TabularInline):
    model = MovieDirector


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    '''Админ панель для фильмов.'''
    list_display = ('title', 'description')
    search_fields = ('title',)
    inlines = (GenreInline, DirectorInline)
