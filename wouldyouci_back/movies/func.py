import os
import pandas as pd
from django.conf import settings
from django.db.models import Count
from django.core.cache import cache
from sklearn.linear_model import Lasso, LinearRegression
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from scipy.stats import uniform as sp_rand
from accounts.models import Rating
from .apps import MoviesConfig
from .models import Movie
from django.contrib.auth import get_user_model
User = get_user_model()


def recommend_userbased(user_id):
    try:
        df = MoviesConfig.knn_pickle
        movie_id_set = df.loc[user_id, 'movie_id'].unique()
        movie_id_set = movie_id_set[:10]
        recommend_movie_set = Movie.objects.filter(id__in=movie_id_set)
    except KeyError:
        print(f'{user_id}가 피클에 없어요. KNN 피클을 업데이트 해야합니다.')
        ratings = Rating.objects.filter(user_id=user_id)
        rating_id_set = ratings.values_list('id', flat=True)

        genre_list = [[i, 0] for i in range(30)]
        for rating in ratings:
            genres = rating.movie.genres.all()
            for g in genres:
                genre_list[g.id][1] += 1

        genre_list = sorted(genre_list, key=lambda x: -x[1])

        genre_id_set = [genre_list[0][0], genre_list[1][0]]
        movies = Movie.objects.filter(genres__in=genre_id_set).exclude(ratings__in=rating_id_set)
        recommend_movie_set = movies.annotate(num_rating=Count('ratings')).order_by('-num_rating', 'score')[:10]

    return recommend_movie_set


def contentsbased_onscreen(user_id):
    genres = MoviesConfig.genre_pickle

    ratings = pd.DataFrame(list(Rating.objects.filter(user=user_id).values('score', 'movie_id')))

    user_profile = ratings.merge(genres, left_on='movie_id', right_index=True)

    model = Lasso()
    param_grid = {'alpha': sp_rand()}

    research = RandomizedSearchCV(estimator=model,
                                  param_distributions=param_grid,
                                  n_iter=30,
                                  cv=5,
                                  random_state=406)

    research.fit(user_profile[genres.columns], user_profile['score'])

    predictions = research.best_estimator_.predict(genres)
    genres.reset_index()

    genres['predict'] = predictions

    onscreen_id_set = Movie.objects.exclude(onscreens=None).exclude(genres=None)
    onscreen_id_set = onscreen_id_set.values_list('id', flat=True)

    score_info = []

    for _id in onscreen_id_set:
        try:
            score_info.append((_id, genres.at[_id, 'predict']))
        except KeyError:
            print(f'{_id}가 피클에 없어요. genre 피클을 업데이트 해야합니다.')

    score_info = sorted(score_info, key=lambda x: -x[1])[:10]
    onscreen_id_set = [x for x, y in score_info]

    return onscreen_id_set


def contentsbased_by_genres_and_directors(user_id, movie_id):
    data = cache.get(f'recommend_{user_id}')
    predicted_score = 0

    if data is None:
        movies = MoviesConfig.movie_pickle

        ratings = pd.DataFrame(list(Rating.objects.filter(user=user_id).values('score', 'movie_id')))
        ratings = ratings.merge(movies, left_on='movie_id', right_index=True)
        x_train, x_test, y_train, y_test = train_test_split(ratings[movies.columns],
                                                            ratings['score'],
                                                            random_state=406,
                                                            test_size=0.1)
        reg = LinearRegression()
        reg.fit(x_train, y_train)

        predictions = reg.predict(movies)
        movies.reset_index()

        movies['predict'] = predictions
        data = movies[['predict']]

        cache.set(f'recommend_{user_id}', data)

    try:
        predicted_score = data.at[movie_id, 'predict']
    except KeyError:
        print(f'{movie_id}가 피클 파일에 없어요. movie 피클을 업데이트 해야합니다.')

    predicted_score = predicted_score - 0.2
    if predicted_score >= 5.0:
        predicted_score = 4.9

    if predicted_score < 0:
        predicted_score = 0.1

    return round(predicted_score * 20, 1)
