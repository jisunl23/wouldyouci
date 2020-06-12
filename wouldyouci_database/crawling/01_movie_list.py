from bs4 import BeautifulSoup
import urllib.request
from datetime import datetime, timedelta
import json

def dateToString(dt):
    res = dt.strftime("%Y%m%d")
    return res

def getPastDate(dt, delta):
    new_date = dt - timedelta(days=delta)
    return new_date

def makeMovieRankURL(option, dt):
    naver_movie_url = 'https://movie.naver.com/movie'
    date_str = dateToString(dt)
    movie_rank_url = naver_movie_url + '/sdb/rank/rmovie.nhn?sel=' + option + '&date=' + date_str
    return movie_rank_url

movie_list = []
check_list = {}

movie_rank_option = ['cnt', 'cur', 'pnt']

yesterday = datetime.today() - timedelta(days=1)

for i in range(365):
    minus_day = i*5
    tg_date = getPastDate(yesterday, minus_day)
    for opt in movie_rank_option:
        url = makeMovieRankURL(opt, tg_date)
        html = urllib.request.urlopen(url)
        soup = BeautifulSoup(html, 'html.parser')

        movie_rank_list = soup.find_all('td', {'class':'title'})
        for mv in movie_rank_list:
            div_tag = mv.find('div')
            a_tag = div_tag.find('a')
            movie_url = a_tag.get('href')
            movie_title = a_tag.get('title')
            check_list[movie_url] = movie_title

with open('01_movie_list.json', 'w', encoding='UTF-8-sig') as fp:
    json.dump(check_list, fp, ensure_ascii=False, indent=4)

# 5월 14일 기준 5일 간격 5년간 데이터 수집 - 3724개
# 조회수 / 현재상영 평점 / 전체 평점 - 5일 간격 상위 50개 데이터