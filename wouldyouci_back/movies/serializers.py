from rest_framework import serializers
from .models import Movie, Onscreen
from accounts.models import Rating
from cinemas.models import Cinema
from django.contrib.auth import get_user_model
User = get_user_model()


class MovieSerializer(serializers.ModelSerializer):
    directors = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
     )
    genres = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
     )
    actors = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
     )

    class Meta:
        model = Movie
        fields = ('id', 'score', 'name', 'name_eng', 'watch_grade', 'running_time', 'summary',
                  'open_date', 'trailer', 'poster', 'directors', 'genres', 'actors')


class TasteMovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ('id', 'name', 'poster')


class SimpleMovieSerializer(serializers.ModelSerializer):
    genres = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
     )

    class Meta:
        model = Movie
        fields = ('id', 'name', 'name_eng', 'poster', 'genres', 'open_date', 'running_time', 'watch_grade')


class SearchMovieSerializer(serializers.ModelSerializer):
    ratings_count = serializers.IntegerField(
        source='ratings.count',
        read_only=True
    )
    genres = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
     )
    actors = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
     )
    directors = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
     )


    class Meta:
        model = Movie
        fields = ('id', 'actors', 'directors', 'name', 'open_date', 'name_eng', 'poster', 'genres', 'running_time', 'watch_grade', 'score', 'ratings_count')


class PremovieSerializer(serializers.ModelSerializer):
    directors = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
     )
    genres = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
     )
    actors = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
     )
    pick_users_count = serializers.IntegerField(
        source='pick_users.count',
        read_only=True
    )

    class Meta:
        model = Movie
        fields = ('id', 'name', 'poster', 'open_date', 'running_time', 'pick_users_count',
                  'genres', 'directors', 'actors')


class OnscreenSerializer(serializers.ModelSerializer):
    movie = SimpleMovieSerializer(read_only=True)
    start_time = serializers.TimeField(format='%H:%M')

    class Meta:
        model = Onscreen
        fields = ('movie', 'info', 'date', 'start_time', 'end_time', 'total_seats', 'seats', 'url')


class RatingPosterSerializer(serializers.ModelSerializer):
    movie = TasteMovieSerializer(read_only=True)

    class Meta:
        model = Rating
        fields = ('id', 'movie', 'score')


class CinemaSerializer(serializers.ModelSerializer):
    onscreens = OnscreenSerializer(many=True, read_only=True)

    class Meta:
        model = Cinema
        fields = ('id', 'name', 'type', 'img', 'address', 'url', 'tel',
                  'public', 'parking', 'onscreens', 'score')


class OnscreenCinemaSerializer(serializers.ModelSerializer):
    onscreens = serializers.StringRelatedField(many=True)

    class Meta:
        model = Cinema
        fields = ('name', 'id', 'tel', 'address', 'url', 'img', 'onscreens')
