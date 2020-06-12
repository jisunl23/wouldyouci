import os
import surprise
import pymysql
import pandas as pd
from decouple import config


def get_genre_info():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    conn = pymysql.connect(host=config('HOST'), port=3306, user=config('USER'),
                           password=config('PASSWORD'), db=config('DB'))
    sql = 'SELECT * FROM wouldyouci.movies_genre'

    result = pd.read_sql_query(sql, conn)

    path = os.path.join(BASE_DIR, 'genres.csv')
    result.to_csv(path, index=True)

    conn.close()


def get_genre_train_data():
    print('트레인 시작')
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    conn = pymysql.connect(host=config('HOST'), port=3306, user=config('USER'),
                           password=config('PASSWORD'), db=config('DB'))
    sql = 'SELECT * FROM wouldyouci.movies_movie_genres'

    movie_genres = pd.read_sql_query(sql, conn, index_col='movie_id')

    path = os.path.join(BASE_DIR, 'genres.csv')
    genres = pd.read_csv(path, index_col='id')

    movie_genres = movie_genres.drop('id', axis='columns')
    movie_genres['genre_id'] = movie_genres['genre_id'].apply(lambda x: genres.loc[x, 'name']+'|')
    movie_genres = movie_genres.groupby('movie_id').sum()

    genres_dummies = movie_genres['genre_id'].str.get_dummies(sep='|')

    path = os.path.join(BASE_DIR, 'genres_train.p')
    genres_dummies.to_pickle(path)

    conn.close()
    print('트레인 끝')


def get_movie_train_data():
    print('트레인 시작')
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    conn = pymysql.connect(host=config('HOST'), port=3306, user=config('USER'),
                           password=config('PASSWORD'), db=config('DB'))
    sql = 'SELECT * FROM wouldyouci.movies_movie_genres'
    sql2 = 'SELECT * FROM wouldyouci.movies_movie_directors'
    sql4 = 'SELECT * FROM wouldyouci.movies_people'

    movie_genres = pd.read_sql_query(sql, conn, index_col='movie_id')
    movie_directors = pd.read_sql_query(sql2, conn, index_col='movie_id')
    people = pd.read_sql_query(sql4, conn, index_col='id')

    path = os.path.join(BASE_DIR, 'genres.csv')
    genres = pd.read_csv(path, index_col='id')

    movie_genres = movie_genres.drop('id', axis='columns')
    movie_directors = movie_directors.drop('id', axis='columns')

    movie_genres['genre_id'] = movie_genres['genre_id'].apply(lambda x: genres.loc[x, 'name'] + '|')
    movie_directors['people_id'] = movie_directors['people_id'].apply(lambda x: people.loc[x, 'name'] + '|')

    movie_genres = movie_genres.groupby('movie_id').sum()
    movie_directors = movie_directors.groupby('movie_id').sum()

    genres_dummies = movie_genres['genre_id'].str.get_dummies(sep='|')
    people_dummies = movie_directors['people_id'].str.get_dummies(sep='|')

    train = people_dummies.merge(genres_dummies, on='movie_id')

    path = os.path.join(BASE_DIR, 'movie_director_train.p')
    train.to_pickle(path)

    conn.close()
    print('트레인 끝')


def recur_dictify(frame):
    if len(frame.columns) == 1:
        if frame.values.size == 1: return frame.values[0][0]
        return frame.values.squeeze()
    grouped = frame.groupby(frame.columns[0])
    d = {k: recur_dictify(g.iloc[:, 1:]) for k, g in grouped}
    return d


def KNN_train():
    print('트레인 시작')
    conn = pymysql.connect(host=config('HOST'), port=3306, user=config('USER'),
                           password=config('PASSWORD'), db=config('DB'))
    sql = 'SELECT * FROM wouldyouci.accounts_rating'
    data = pd.read_sql_query(sql, conn)
    conn.close()
    df = data[['user_id', 'movie_id', 'score']]

    n1 = 5
    filter_movies = df['movie_id'].value_counts() >= n1
    filter_movies = filter_movies[filter_movies].index.tolist()

    n2 = 5
    filter_users = df['user_id'].value_counts() >= n2
    filter_users = filter_users[filter_users].index.tolist()

    df_new = df[df['movie_id'].isin(filter_movies) & df['user_id'].isin(filter_users)]

    df_to_dict = recur_dictify(df_new)

    user_list = []
    movie_set = set()

    for user in df_to_dict:
        user_list.append(user)

        for movie in df_to_dict[user]:
            movie_set.add(movie)

    movie_list = list(movie_set)

    rating_dic = {
        'user_id': [],
        'movie_id': [],
        'score': []
    }

    for user in df_to_dict:
        for movie in df_to_dict[user]:
            u_index = user_list.index(user)
            m_index = movie_list.index(movie)
            score = df_to_dict[user][movie]

            rating_dic['user_id'].append(u_index)
            rating_dic['movie_id'].append(m_index)
            rating_dic['score'].append(score)

    df = pd.DataFrame(rating_dic)

    reader = surprise.Reader(rating_scale=(0.5, 5.0))

    col_list = ['user_id', 'movie_id', 'score']
    data = surprise.Dataset.load_from_df(df_new[col_list], reader)

    trainset = data.build_full_trainset()

    option = {'name': 'pearson'}
    algo = surprise.KNNBasic(sim_options=option)
    algo.fit(trainset)

    recommand_dic = {
        'user_id': [],
        'movie_id': [],
    }

    for user_key in df_new['user_id'].unique():
        index = user_list.index(user_key)
        result = algo.get_neighbors(index, k=5)
        recom_set = set()
        for i in result:
            max_rating = data.df[data.df['user_id'] == user_list[i]]['score'].max()
            recom_movies = data.df[(data.df['score'] == max_rating) & (data.df['user_id'] == user_list[i])][
                'movie_id'].values
            for item in recom_movies:
                recom_set.add(item)

            for item in recom_set:
                recommand_dic['user_id'].append(user_key)
                recommand_dic['movie_id'].append(item)

    pickle = pd.DataFrame(recommand_dic)

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(BASE_DIR, 'KNN.p')

    pd.to_pickle(pickle, path)
    print('트레인 끝')
