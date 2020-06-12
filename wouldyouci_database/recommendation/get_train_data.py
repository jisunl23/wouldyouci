import os
import pymysql
import surprise
import pandas as pd
from decouple import config
from datetime import datetime


# 장르만
def get_train_data(BASE_DIR):
    print('장르 학습 시작')
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
    print('종료')


# 장르 + 영화인 전부
def get_train_data2(BASE_DIR):
    print('장르 + 영화인 전부 학습 시작')
    conn = pymysql.connect(host=config('HOST'), port=3306, user=config('USER'),
                           password=config('PASSWORD'), db=config('DB'))
    sql = 'SELECT * FROM wouldyouci.movies_movie_genres'
    sql2 = 'SELECT * FROM wouldyouci.movies_movie_directors'
    sql3 = 'SELECT * FROM wouldyouci.movies_movie_actors'
    sql4 = 'SELECT * FROM wouldyouci.movies_people'

    movie_genres = pd.read_sql_query(sql, conn, index_col='movie_id')
    movie_directors = pd.read_sql_query(sql2, conn, index_col='movie_id')
    movie_actors = pd.read_sql_query(sql3, conn, index_col='movie_id')
    people = pd.read_sql_query(sql4, conn, index_col='id')

    path = os.path.join(BASE_DIR, 'genres.csv')
    genres = pd.read_csv(path, index_col='id')

    movie_people = pd.concat([movie_directors, movie_actors])

    movie_genres = movie_genres.drop('id', axis='columns')
    movie_people = movie_people.drop('id', axis='columns')

    movie_genres['genre_id'] = movie_genres['genre_id'].apply(lambda x: genres.loc[x, 'name'] + '|')
    movie_people['people_id'] = movie_people['people_id'].apply(lambda x: people.loc[x, 'name'] + '|')

    movie_genres = movie_genres.groupby('movie_id').sum()
    movie_people = movie_people.groupby('movie_id').sum()

    genres_dummies = movie_genres['genre_id'].str.get_dummies(sep='|')
    people_dummies = movie_people['people_id'].str.get_dummies(sep='|')

    train = people_dummies.merge(genres_dummies, on='movie_id')

    path = os.path.join(BASE_DIR, 'movie_train.p')
    train.to_pickle(path)
    conn.close()
    print('종료')


# 장르 + 감독만
def get_train_data3(BASE_DIR):
    print('장르 + 감독 학습 시작')
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
    print('종료')


# 장르 테이블 가져오기
def get_genre_info(BASE_DIR):
    conn = pymysql.connect(host=config('HOST'), port=3306, user=config('USER'),
                           password=config('PASSWORD'), db=config('DB'))
    sql = 'SELECT * FROM wouldyouci.movies_genre'
    result = pd.read_sql_query(sql, conn)

    path = os.path.join(BASE_DIR, 'genres.csv')
    result.to_csv(path, index=True)

    conn.close()


def KNN_train(BASE_DIR):
    print('KNN 학습 시작 : ', str(datetime.now())[10:19])
    conn = pymysql.connect(host=config('HOST'), port=3306, user=config('USER'),
                           password=config('PASSWORD'), db=config('DB'))
    sql = 'SELECT * FROM wouldyouci.accounts_rating'
    data = pd.read_sql_query(sql, conn)
    conn.close()
    df = data[['user_id', 'movie_id', 'score']]

    # 리뷰 n개 이상 달린 영화
    # 5개 이상 달린 영화
    n1 = 5
    filter_movies = df['movie_id'].value_counts() >= n1
    filter_movies = filter_movies[filter_movies].index.tolist()

    # n개 이상 평가한 유저
    n2 = 5
    filter_users = df['user_id'].value_counts() >= n2
    filter_users = filter_users[filter_users].index.tolist()

    df_new = df[df['movie_id'].isin(filter_movies) & df['user_id'].isin(filter_users)]

    df_to_dict = recur_dictify(df_new)

    user_list = []
    movie_set = set()
    # 유저 수 만큼 반복한다
    for user in df_to_dict:
        user_list.append(user)

        # 현재 사용자가 본 영화 목록을 set에 담는다.
        for movie in df_to_dict[user]:
            movie_set.add(movie)

    movie_list = list(movie_set)

    # 학습할 데이터를 준비한다.
    rating_dic = {
        'user_id': [],
        'movie_id': [],
        'score': []
    }

    # 유저 수 만큼 반복
    for user in df_to_dict:
        # 해당 유저가 본 영화 수 만큼 반복
        for movie in df_to_dict[user]:
            # 유저 인덱스 번호를 추출
            u_index = user_list.index(user)

            # 영화 인덱스 번호를 추출
            m_index = movie_list.index(movie)

            # 평점을 가져온다
            score = df_to_dict[user][movie]

            # 딕셔너리에 담는다
            rating_dic['user_id'].append(u_index)
            rating_dic['movie_id'].append(m_index)
            rating_dic['score'].append(score)

    # 데이터셋 만들기
    df = pd.DataFrame(rating_dic)

    # 학습
    reader = surprise.Reader(rating_scale=(0.5, 5.0))

    # surprise에서 사용할 데이터셋을 구성할 때 필요한 이름
    # 데이터가 저장되어 있는 딕셔너리의 컬럼 이름
    col_list = ['user_id', 'movie_id', 'score']
    data = surprise.Dataset.load_from_df(df_new[col_list], reader)

    # 학습한다
    trainset = data.build_full_trainset()
    # Pearson similarity 사용
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

    path = os.path.join(BASE_DIR, 'KNN.p')
    pd.to_pickle(pickle, path)

    print('종료 : ', str(datetime.now())[10:19])


# 테이블을 딕셔너리로 만드는 함수
def recur_dictify(frame):
    if len(frame.columns) == 1:
        if frame.values.size == 1: return frame.values[0][0]
        return frame.values.squeeze()
    grouped = frame.groupby(frame.columns[0])
    d = {k: recur_dictify(g.iloc[:, 1:]) for k, g in grouped}
    return d


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

get_genre_info(BASE_DIR)
get_train_data(BASE_DIR)
get_train_data2(BASE_DIR)
get_train_data3(BASE_DIR)
KNN_train(BASE_DIR)
