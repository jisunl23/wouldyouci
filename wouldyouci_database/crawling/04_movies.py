from bs4 import BeautifulSoup
import urllib.request
from datetime import datetime, timedelta
from dotenv import load_dotenv
import json
import requests
import pyperclip
import time

import os
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

from selenium import webdriver

# Explicitly wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# chromedriver_dir=r'C:\Users\multicampus\Downloads\chromedriver\chromedriver.exe'
# driver = webdriver.Chrome(chromedriver_dir)

with open('02_movie_list_save.json', 'r', encoding='UTF-8') as fr:
    movie_list = json.load(fr)

with open('03_genre.json', 'r', encoding='UTF-8') as fr:
    genre_dict = json.load(fr)

def getCodeFromURL(movie_url):
    equal_idx = movie_url.index('=')
    movie_code = movie_url[equal_idx+1:]
    return movie_code

def deleteBTag(movie_name):
    ck = False
    res = movie_name
    for idx in range(len(movie_name)-3):
        if movie_name[idx:idx+3] == '<b>':
            btag_start = movie_name.index('<b>')
            btag_end = movie_name.index('</b>')
            res = movie_name[btag_start+3:btag_end]
            break
    return res

def findGenreCode(movie_genre):
    pk_list = []
    for genre_name in movie_genre:
        for genre in genre_dict:
            if genre['fields']['name'] == genre_name:
                pk_list.append(genre['pk'])
    return pk_list

def getInfoDict(atag_list, movie_info):
    atag_dict = {}
    atag_dict['watch_grade'] = ''
    atag_dict['open_date'] = movie_info['pubDate']
    atag_dict['genres'] = []
    for idx in range(len(atag_list)):
        info_atag = atag_list[idx]
        info_href = info_atag.get('href')
        if info_href != '#':
            question_idx = info_href.index('?')
            equal_idx = info_href.index('=')
            if question_idx and equal_idx:
                query = info_href[question_idx+1: equal_idx]
                if query == 'grade':
                    if not atag_dict['watch_grade']:
                        atag_dict['watch_grade'] = info_atag.text
                elif query == 'open':
                    open_date = info_href[equal_idx+1:]
                    if len(open_date) > 4:
                        open_date = open_date[:4] + '-' + open_date[4:6] + '-' + open_date[6:]
                    atag_dict['open_date'] = open_date
                elif query == 'genre':
                    genre_pk = info_href[equal_idx+1:]
                    atag_dict['genres'].append(int(genre_pk))
    if not atag_dict['watch_grade']:
        atag_dict['watch_grade'] = '정보없음'
    return atag_dict

def getPeopleInfo(people_area):
    directors = []
    actors = []
    people_json = {}
    if people_area:
        people_list = people_area.find_all('li')
        for people in people_list:
            dt_tag = people.find('dt')
            dt_class = dt_tag.get('class')
            a_tag = people.find('a', {'class': 'tx_people'})
            if a_tag:
                a_href = a_tag.get('href')
                people_code = int(getCodeFromURL(a_href))
                if dt_class[0] == 'staff_dir':
                    directors.append(people_code)
                elif dt_class[0] == 'staff_main':
                    actors.append(people_code)
                
                people_json[people_code] = a_tag.get('title')

    people_dict = {}
    people_dict['directors'] = directors
    people_dict['actors'] = actors

    return people_dict, people_json

def getRunTime(tg_area):
    span_tags = tg_area.find_all('span')
    for span_tag in span_tags:
        span_text = span_tag.text
        if '분' in span_text:
            return span_text

def copyInput(self, xpath, input_text):
    pyperclip.copy(input_text)
    driver.find_element_by_xpath(xpath).click()
    ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
    time.sleep(1)

def getSummary(desc):
    cutpoint = 0
    new_desc = desc
    for idx in range(len(desc)-3):
        if desc[idx:idx+3] == '줄거리':
            cutpoint = idx
            new_desc = new_desc[cutpoint+5:]
            break
    for idx in range(len(new_desc)):
        if new_desc[idx] == '\r':
            new_desc = new_desc[:idx] + '\n' + new_desc[idx+1:]
    
    double_point = []
    for i in range(len(new_desc)-1):
        if new_desc[i] == '\n' and new_desc[i+1] == '\n':
            double_point.append(i+1)
    
    res = ''
    s_point = 0
    for idx in double_point:
        res += new_desc[s_point:idx]
        s_point = idx+1
    if s_point < len(new_desc):
        res += new_desc[s_point:]
    
    for idx in range(len(res)-4):
        if res[idx:idx+4] == '제작노트':
            res = res[:idx-1]
            break
    return res


def getTrailer(title, s_opt):
    res = ''
    YOUTUBE_KEY = os.getenv('YOUTUBE_KEY6')
    REQUEST_URL = 'https://www.googleapis.com/youtube/v3/search?'
    YOUTUBE_SEARCH = 'https://www.youtube.com/results?'
    options = {
        'key': YOUTUBE_KEY,
        'part': 'id',
        'q': title + ' ' + s_opt,
        'maxResults': 1,
        'type': 'video',
        'videoDuration': 'short'
    }
    search_option = {
        'search_query': title + ' ' + s_opt,
    }
    # TITLE_TO_URL = urllib.parse.urlencode(search_option)
    # SEARCH_URL = YOUTUBE_SEARCH + TITLE_TO_URL
    # y_html = urllib.request.urlopen(SEARCH_URL)
    # y_soup = BeautifulSoup(y_html, 'lxml')
    # atags = y_soup.find_all('a')
    # if atags:
    #     for atag in atags:
    #         href_url = atag.get('href')
    #         break
    url_option = urllib.parse.urlencode(options)
    SEARCH_URL = REQUEST_URL+url_option
    SEARCH_RESULT = json.loads(urllib.request.urlopen(SEARCH_URL).read())
    ITEM_LIST = SEARCH_RESULT['items']
    if ITEM_LIST:
        YOUTUBE_VIDEO_URL = 'https://www.youtube.com/embed/'
        for ITEM in ITEM_LIST:
            if ITEM['id'].get('videoId'):
                youtube_code = ITEM['id']['videoId']
                break
        res = YOUTUBE_VIDEO_URL + youtube_code
    return res

chromedriver_dir=r'C:\Users\multicampus\Downloads\chromedriver\chromedriver.exe'
driver = webdriver.Chrome(chromedriver_dir)

load_dotenv(verbose=True)
NAVER_CLIENT_ID = os.getenv('NAVER_CLIENT_ID')
NAVER_CLIENT_SECRET = os.getenv('NAVER_CLIENT_SECRET')
NAVER_REQUEST_URL = 'https://openapi.naver.com/v1/search/movie.json?'
header={
    "X-Naver-Client-Id":NAVER_CLIENT_ID,
    "X-Naver-Client-secret":NAVER_CLIENT_SECRET,
}

NAVER_MOVIE = 'https://movie.naver.com'
NAVER_IMAGE_URL = 'https://movie.naver.com/movie/bi/mi/photoViewPopup.nhn?movieCode='
NAVER_ID = os.getenv('NAVER_ID')
NAVER_PW = os.getenv('NAVER_PW')
movie_cnt = 0

for detail_url, title in movie_list.items():
    movie_pk = getCodeFromURL(detail_url)
    check = True

    with open('04_complete_save.json', 'r', encoding='UTF-8') as fr:
        complete_movie = json.load(fr)
    if complete_movie.get(movie_pk):
        continue

    with open('04_notfound_save.json', 'r', encoding='UTF-8') as fr:
        not_found = json.load(fr)
    if not_found.get(movie_pk):
        continue

    with open('04_movies_save.json', 'r', encoding='UTF-8') as fr:
        movies = json.load(fr)
    with open('04_peoples_save.json', 'r', encoding='UTF-8') as fr:
        peoples = json.load(fr)

    url = NAVER_MOVIE + detail_url
    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html, 'lxml')

    driver.get(url)
    sel_source = driver.page_source          
    sel_soup = BeautifulSoup(sel_source, 'html.parser')
    needlogin = sel_soup.find('form', {'id': 'frmNIDLogin'})

    if needlogin:
        IDxPath='//*[@id="id"]'
        PasswordxPath='//*[@id="pw"]'

        ID=NAVER_ID
        Password=NAVER_PW

        copyInput(driver, IDxPath, ID)
        copyInput(driver,PasswordxPath,Password)
        driver.find_element_by_xpath('//*[@value="로그인"]').click()
        time.sleep(1)
        source = driver.page_source          
        soup = BeautifulSoup(source, 'html.parser')
        
    req = requests.get(NAVER_REQUEST_URL+"query="+title+"&display=100", headers = header).json()
    req_items = req['items']
    for item in req_items:
        if item['link'] == url:
            check = False
            tg_movie = item
            info_area = soup.find('dl', {'class': 'info_spec'})
            info_atag = info_area.find_all('a')
            genres = []
            watch_grade = ''
            info_dict = getInfoDict(info_atag, tg_movie)
            running_time = getRunTime(info_area)
            people_area = soup.find('div', {'class': 'people'})
            people_dict, new_people = getPeopleInfo(people_area)

            description = soup.find('div', {'class': 'story_area'})
            if description:
                summary = getSummary(description.text)
            else:
                summary = ''

            new_movie_info = {}
            new_movie_info['model'] = "movies.movie"
            new_movie_info['pk'] = int(movie_pk)

            new_fields = {
                'name': '',
                'name_eng': '',
                'watch_grade': '',
                'running_time': '',
                'summary': '',
                'open_date': '',
                'trailer': '',
                'poster': '',
                'directors': [],
                'genres': [],
                'actors': []
            }


            new_fields['name'] = title
            new_fields['name_eng'] = tg_movie['subtitle']
            new_fields['summary'] = summary
            # if tg_movie['subtitle']:
            #     new_fields['trailer'] = getTrailer(tg_movie['subtitle'], 'trailer')
            # else:
            #     new_fields['trailer'] = getTrailer(title, '예고편')
            new_fields['trailer'] = ''
            image_url = NAVER_IMAGE_URL+movie_pk
            image_html = urllib.request.urlopen(image_url)
            image_soup = BeautifulSoup(image_html, 'lxml')
            image_tag = image_soup.find('img', {'id': 'targetImage'})
            
            if image_tag:
                image_src = image_tag.get('src')
                new_fields['poster'] = image_src
            elif tg_movie['image']:
                new_fields['poster'] = tg_movie['image']
            else:
                new_fields['poster'] = ''

            if running_time:
                new_fields['running_time'] = running_time[:-1]
            else:
                new_fields['running_time'] = '정보없음'

            for k, v in info_dict.items():
                new_fields[k] = v
            for k, v in people_dict.items():
                new_fields[k] = v
            for k, v in new_people.items():
                peoples[k] = v
            new_movie_info['fields'] = new_fields
            movies.append(new_movie_info)
            complete_movie[movie_pk] = title
            movie_cnt += 1
            break

    if check:
        not_found[movie_pk] = title
        with open('04_notfound_save.json', 'w', encoding='UTF-8') as fp:
            json.dump(not_found, fp, ensure_ascii=False, indent=4)

    with open('04_movies_save.json', 'w', encoding='UTF-8') as fp:
        json.dump(movies, fp, ensure_ascii=False, indent=4)

    with open('04_peoples_save.json', 'w', encoding='UTF-8') as fp:
        json.dump(peoples, fp, ensure_ascii=False, indent=4)
    
    with open('04_complete_save.json', 'w', encoding='UTF-8') as fp:
        json.dump(complete_movie, fp, ensure_ascii=False, indent=4)

    
driver.quit()
with open('04_movies.json', 'w', encoding='UTF-8') as fp:
    json.dump(movies, fp, ensure_ascii=False, indent=4)

with open('04_peoples.json', 'w', encoding='UTF-8') as fp:
    json.dump(peoples, fp, ensure_ascii=False, indent=4)

print('******************끝***************************')