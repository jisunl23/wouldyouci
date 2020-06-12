from django.db import models
from cinemas.models import Cinema


class Genre(models.Model):
    name = models.CharField(max_length=150)


class People(models.Model):
    name = models.CharField(max_length=50)


class Movie(models.Model):
    name = models.CharField(max_length=150)
    name_eng = models.CharField(max_length=150, blank=True, null=True)
    watch_grade = models.CharField(max_length=150)
    running_time = models.CharField(max_length=50)
    summary = models.TextField()
    open_date = models.CharField(max_length=20, blank=True, null=True)

    trailer = models.CharField(max_length=200, blank=True, null=True)
    poster = models.CharField(max_length=200, blank=True, null=True)

    directors = models.ManyToManyField(People, related_name='movie_directors')
    genres = models.ManyToManyField(Genre, related_name='movie_genres')
    actors = models.ManyToManyField(People, related_name='movie_actors')

    score = models.FloatField(blank=True, default=0)


class Onscreen(models.Model):
    movie = models.ForeignKey(Movie, blank=True, null=True, on_delete=models.CASCADE, related_name='onscreens')
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE, related_name='onscreens')
    info = models.CharField(max_length=50)
    date = models.DateField(auto_now_add=False, auto_now=False)
    start_time = models.TimeField(auto_now_add=False, auto_now=False)
    end_time = models.CharField(max_length=20, blank=True, null=True)
    total_seats = models.CharField(max_length=5)
    seats = models.CharField(max_length=5)
    url = models.URLField(max_length=250, blank=True, null=True)
    cm_code = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ('start_time',)

    def __str__(self):
        return '%s' % self.start_time


class Premovie(models.Model):
    name = models.CharField(max_length=150)
    name_eng = models.CharField(max_length=150, blank=True, null=True)

    running_time = models.CharField(max_length=50)
    summary = models.TextField()
    open_date = models.CharField(max_length=20)

    poster = models.CharField(max_length=200, blank=True, null=True)

    directors = models.CharField(max_length=150)
    genres = models.ManyToManyField(Genre, related_name='premovie_genres')
    actors = models.CharField(max_length=150)
