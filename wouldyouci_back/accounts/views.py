from datetime import date, timedelta
from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from cinemas.serializers import SimpleCinemaSerializer
from movies.models import Movie
from movies.serializers import TasteMovieSerializer, RatingPosterSerializer, SimpleMovieSerializer
from movies.func import contentsbased_onscreen, recommend_userbased
from .models import Profile
from .serializers import UserCreationSerializer, UserDetailSerializer, ProfileSerializer, RatingSerializer
from django.contrib.auth import get_user_model
User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def create_user(request):
    if request.method == 'POST':
        serializer = UserCreationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(user.password)
            user.save()
            return Response(status=200, data={'message': '회원가입 되었습니다.'})

        return Response(status=400, data={'message': serializer.errors})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_rating_tf(request):
    user = request.user
    rating_cnt = user.ratings.count()
    rating_tf = False
    if user.ratings.count() > 9:
        rating_tf = True

    dataset = {
        'rating_tf': rating_tf,
        'rating_cnt': rating_cnt
    }

    return Response(status=200, data=dataset)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_index(request):

    user = request.user
    user_serializer = UserDetailSerializer(user)
    pick_movies = user.pick_movies.all()

    today = date.today()
    push_movies = pick_movies.filter(open_date__gt=today + timedelta(days=1))
    pick_movies = pick_movies.filter(open_date__lte=today + timedelta(days=1))

    pick_cinemas = user.pick_cinemas.all()
    push_movies_serializer = SimpleMovieSerializer(push_movies, many=True)
    pick_movies_serializer = SimpleMovieSerializer(pick_movies, many=True)
    pick_cinemas_serializer = SimpleCinemaSerializer(pick_cinemas, many=True)

    rating_tf = False
    recommend_movies = []
    recommend_onscreen = []
    recommend_movies_cnt = 0
    recommend_onscreen_cnt = 0
    if user.ratings.count() > 9:
        rating_tf = True

        recommend_movie_set = recommend_userbased(user.id)
        recommend_serializer = SimpleMovieSerializer(recommend_movie_set, many=True)
        recommend_movies = recommend_serializer.data
        recommend_movies_cnt = recommend_movie_set.count()

        onscreen_id_set = contentsbased_onscreen(user.id)
        onscreen_movie_set = Movie.objects.filter(id__in=onscreen_id_set)
        onscreen_serializer = SimpleMovieSerializer(onscreen_movie_set, many=True)
        recommend_onscreen = onscreen_serializer.data
        recommend_onscreen_cnt = onscreen_movie_set.count()

    dataset = {
        'meta': {
            'rating_tf': rating_tf,
            'pick_cinemas': pick_cinemas.count(),
            'pick_movies': pick_movies.count(),
            'push_movies': push_movies.count(),
            'recommend_movies': recommend_movies_cnt,
            'recommend_onscreen': recommend_onscreen_cnt,
        },
        'data': {
            'user': user_serializer.data,
            'pick_cinemas': pick_cinemas_serializer.data,
            'pick_movies': pick_movies_serializer.data,
            'push_movies': push_movies_serializer.data,
            'recommend_movies': recommend_movies,
            'recommend_onscreen': recommend_onscreen
        }
    }

    return Response(status=200, data=dataset)


@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def change_profile(request):
    user = request.user
    if user.file.exists():
        profile = Profile.objects.get(user=user.id)
        profile.delete()
    if request.method == 'POST':
        if request.FILES:
            serializer = ProfileSerializer(request.POST, request.FILES)
            if serializer.is_valid():
                profile = serializer.create(serializer.validated_data)
                profile.user_id = user.id
                profile.save()
                return Response(status=200, data={'file': f"media/{profile.file}"})
            return Response(status=400, data={'message': '유효하지 않은 파일입니다.'})
        return Response(status=403, data={'message': '이미지는 필수입니다.'})
    elif request.method == 'DELETE':
        return Response(status=204)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = get_object_or_404(User, id=request.user.id)
    new_password = request.data.get('new_password')

    if not new_password:
        return Response(status=400, data={'message': '필수 데이터가 누락되었습니다.'})

    user.set_password(new_password)
    user.save()
    return Response(status=203)


class SmallPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = "page_size"
    max_page_size = 60


class TasteViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TasteMovieSerializer
    pagination_class = SmallPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        id_set = [21, 25, 29, 9]
        rated_id = user.ratings.values_list('movie', flat=True)
        queryset = (
            Movie.objects
                .exclude(id__in=rated_id)
                .exclude(genres__in=id_set)
                .exclude(watch_grade='청소년 관람불가')
                .filter(open_date__gte='2015')
                .annotate(num_rating=Count('ratings'))
                .order_by('-num_rating', '-score')
        )
        return queryset


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def get_create_dummy_rating(request):
    user = request.user
    if request.method == 'GET':
        ratings = user.ratings.all()
        serializer = RatingPosterSerializer(ratings, many=True)
        return Response(status=200, data=serializer.data)

    elif request.method == 'POST':
        for data in request.data['data']:
            if user.ratings.filter(movie=data['movie']).exists():
                continue

            serializer = RatingSerializer(data=data)
            if serializer.is_valid():
                new_rating = serializer.save(user=user)
                movie = new_rating.movie
                ratings_count = movie.ratings.count()
                movie_rating = movie.score * (ratings_count - 1)
                movie_rating = (movie_rating + new_rating.score) / ratings_count
                movie.score = movie_rating
                movie.save()
            else:
                return Response(status=400, data=serializer.errors)

        return Response(status=203)
