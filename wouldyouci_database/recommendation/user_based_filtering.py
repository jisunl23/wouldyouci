import os
import pandas as pd


def userbased(user_id):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(BASE_DIR, 'KNN.p')
    df = pd.read_pickle(path)
    return df.loc[df['user_id'] == user_id	, 'movie_id'].unique()


k = userbased(9000009)
print('영화 id 목록 :', k)
