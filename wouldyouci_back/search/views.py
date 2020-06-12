from django.db.models import Count
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from movies.serializers import SimpleMovieSerializer, SearchMovieSerializer, PremovieSerializer
from movies.models import Movie
from cinemas.models import Cinema
from cinemas.serializers import SearchCinemaSerializer
from .documents import MoviesDocument
from datetime import date, timedelta
from haversine import haversine


@api_view(['GET'])
@permission_classes([AllowAny])
def autocomplete_movie(request):
    words = request.query_params.get('words')

    if not words:
        return Response(status=203, data=[])

    movies = Movie.objects.filter(name__startswith=words[0])

    for w in words:
        movies = movies.filter(name__contains=w)

    results = movies.values_list('name', flat=True).distinct()

    return Response(status=200, data=results[:10])


@api_view(['GET'])
@permission_classes([AllowAny])
def search_movie(request, words):

    s4 = MoviesDocument.search().query({
        "bool": {
            "should": [
                {"match": {"name": {"query": words, "boost": 20}}},
                {"match": {"summary": {"query": words}}},
            ]
        }
    })

    id_set = [hit.id for hit in s4]

    search_movies = []
    for _id in id_set:
        movie = Movie.objects.get(id=_id)
        serializer = SimpleMovieSerializer(movie)
        search_movies.append(serializer.data)

    sim_movies = Movie.objects.exclude(id__in=id_set).filter(name__startswith=words[0])

    for w in words:
        sim_movies = sim_movies.filter(name__contains=w)

    sim_serializer = SimpleMovieSerializer(sim_movies, many=True)

    dataset = {
        'meta': {
            'search_result': len(id_set),
            'similar_result': sim_movies.count()
        },
        'search_result': search_movies,
        'similar_result': sim_serializer.data
    }

    return Response(status=200, data=dataset)


@api_view(['GET'])
@permission_classes([AllowAny])
def autocomplete_cinema(request):
    words = request.query_params.get('words')

    if not words:
        return Response(status=203, data=[])

    cinemas = Cinema.objects.filter(area__contains=words[0])

    for w in words:
        cinemas = cinemas.filter(area__contains=w)

    results = cinemas.values_list('area', flat=True).distinct()

    return Response(status=200, data=results[:10])


@api_view(['GET'])
@permission_classes([AllowAny])
def search_cinema(request, words):
    cinemas = Cinema.objects.filter(area__contains=words)

    id_set = cinemas.values_list('id', flat=True)
    sim_cinemas = Cinema.objects.exclude(id__in=id_set).filter(address__contains=words)

    serializer = SearchCinemaSerializer(cinemas, many=True)
    sim_serializer = SearchCinemaSerializer(sim_cinemas, many=True)

    dataset = {
        'meta': {
            'search_result': cinemas.count(),
            'similar_result': sim_cinemas.count(),
        },
        'search_result': serializer.data,
        'similar_result': sim_serializer.data,
    }

    return Response(status=200, data=dataset)


@api_view(['GET'])
@permission_classes([AllowAny])
def search_index(request):
    x = float(request.query_params.get('x', 0))
    y = float(request.query_params.get('y', 0))

    near_cinema = []
    if x and y:
        position = (y, x)
        cinemas = Cinema.objects.filter(
            y__range=(y - 0.01, y + 0.01),
            x__range=(x - 0.015, x + 0.015)
        )

        id_set = [cinema.id for cinema in cinemas
                  if haversine(position, (float(cinema.y), float(cinema.x))) <= 2]

        for _id in id_set:
            cinema = Cinema.objects.get(id=_id)
            serializer = SearchCinemaSerializer(cinema)
            near_cinema.append(serializer.data)

    today = date.today()

    comming_soon = Movie.objects.filter(open_date__gte=today,
                                        open_date__lte=today + timedelta(days=62)).order_by('open_date')
    soon_serializer = PremovieSerializer(comming_soon, many=True)

    popular_movies = Movie.objects.exclude(onscreens=None).annotate(num_rating=Count('ratings'))
    popular_movies = popular_movies.order_by('-num_rating')[:10]
    pop_serializer = SearchMovieSerializer(popular_movies, many=True)

    dataset = {
        'meta': {
            'near_cinema': len(near_cinema),
            'popular_movies': len(popular_movies),
            'comming_soon': len(comming_soon),
        },
        'near_cinema': near_cinema,
        'popular_movies': pop_serializer.data,
        'comming_soon': soon_serializer.data,
    }

    return Response(status=200, data=dataset, content_type='application.json')
