from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.core.cache import cache
from accounts.serializers import RatingSerializer, SimpleRatingSerializer
from accounts.models import Rating
from cinemas.serializers import SearchCinemaSerializer
from cinemas.models import Cinema
from .models import Movie
from .serializers import MovieSerializer
from .func import contentsbased_by_genres_and_directors
from django.contrib.auth import get_user_model
User = get_user_model()


class SmallPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50


class RatingViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SimpleRatingSerializer
    pagination_class = SmallPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        movie_id = self.request.query_params.get('movie', 0)
        movie = get_object_or_404(Movie, id=movie_id)
        queryset = (
            movie.ratings.all()
        )
        return queryset


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    serializer = MovieSerializer(movie)
    user = request.user
    has_score = user.ratings.filter(movie=movie_id).exists()
    pick_movies = user.pick_movies.filter(id=movie_id).exists()

    predicted_score = 0

    if user.ratings.count() > 9:
        predicted_score = contentsbased_by_genres_and_directors(user.id, movie_id)

    dataset = {
        'has_score': has_score,
        'pick_movies': pick_movies,
        'is_showing': movie.onscreens.exists(),
        'predicted_score': predicted_score,
    }
    dataset.update(serializer.data)

    return Response(status=200, data=dataset)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def pick_movie(request, movie_id):
    user = request.user
    movie = get_object_or_404(Movie, id=movie_id)
    if movie.pick_users.filter(id=user.id).exists():
        movie.pick_users.remove(user)
        return Response(status=200, data={"pick_movies": False})
    else:
        movie.pick_users.add(user)
        return Response(status=200, data={"pick_movies": True})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_rating(request):
    user = request.user
    if user.ratings.filter(movie=request.data['movie']).exists():
        return Response(status=403, data={'message': '이미 평가한 영화입니다.'})

    serializer = RatingSerializer(data=request.data)
    if serializer.is_valid():

        cache.delete(f'recommend_{user.id}')
        new_rating = serializer.save(user=user)

        movie = new_rating.movie
        ratings_count = movie.ratings.count()
        movie_rating = movie.score * (ratings_count - 1)
        movie_rating = (movie_rating + new_rating.score) / ratings_count
        movie.score = movie_rating
        movie.save()

        new_rating_serializer = SimpleRatingSerializer(new_rating)

        return Response(new_rating_serializer.data)
    return Response(status=400, data=serializer.errors)


@api_view(['PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def patch_delete_rating(request, rating_id):
    rating = get_object_or_404(Rating, id=rating_id)
    origin_score = rating.score
    movie = rating.movie
    ratings_count = movie.ratings.count()
    movie_rating = movie.score * ratings_count - origin_score

    user_id = request.user.id
    if rating.user.id == user_id:
        if request.method == 'PATCH':
            serializer = RatingSerializer(instance=rating, data=request.data)
            if serializer.is_valid():

                cache.delete(f'recommend_{user_id}')
                update_rating = serializer.save()

                movie_rating = (movie_rating + update_rating.score) / ratings_count
                movie.score = movie_rating
                movie.save()

                new_rating_serializer = SimpleRatingSerializer(update_rating)

                return Response(new_rating_serializer.data)
            return Response(status=400, data=serializer.errors)

        elif request.method == 'DELETE':
            cache.delete(f'recommend_{user_id}')
            rating.delete()

            if ratings_count - 1:
                movie_rating = movie_rating / (ratings_count - 1)
            else:
                movie_rating = 0

            movie.score = movie_rating
            movie.save()

            return Response(status=204)

    return Response(status=400, data={'message': '권한이 없습니다.'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_onscreen_cinema(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    cinema_id_set = movie.onscreens.values_list('cinema', flat=True).distinct()
    cinemas = Cinema.objects.filter(id__in=cinema_id_set)
    area = list(cinemas.values_list('area', flat=True).distinct())
    serializer = SearchCinemaSerializer(cinemas, many=True)

    dataset = {
        'area': area,
        'data': serializer.data
    }

    return Response(status=200, data=dataset)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_rating_avg(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    score = movie.score
    if score:
        score = round(score, 2)
    else:
        score = 0
    return Response(status=200, data={'score': score})
