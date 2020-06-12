from bs4 import BeautifulSoup
import urllib.request
from dotenv import load_dotenv
import json
import requests
import pyperclip 
import time
import datetime

import os
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

def copyInput(self, xpath, input_text):
    pyperclip.copy(input_text)
    driver.find_element_by_xpath(xpath).click()
    ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
    time.sleep(1)

def getMovieName(tg_str):
    end_idx = tg_str.index(']')
    res = tg_str[end_idx+2:]
    for i in range(len(res)):
        if res[i] == '/':
            res = res[:i]
            break
    return res

def deleteGwal(tg_str):
    end_idx = tg_str.index(')')
    return tg_str[end_idx+1:]

def getCodeFromURL(movie_url):
    equal_idx = movie_url.index('=')
    movie_code = movie_url[equal_idx+1:]
    return movie_code

def getDirectorName(tg_str):
    idx = len(tg_str)
    for i in range(len(tg_str)):
        if tg_str[i] == '|':
            idx = i
            break
    return tg_str[:idx]

def getNaverInfo(movie_name, director_name):
    NAVER_CLIENT_ID = os.getenv('NAVER_CLIENT_ID')
    NAVER_CLIENT_SECRET = os.getenv('NAVER_CLIENT_SECRET')
    NAVER_REQUEST_URL = 'https://openapi.naver.com/v1/search/movie.json?'
    header={
        "X-Naver-Client-Id":NAVER_CLIENT_ID,
        "X-Naver-Client-secret":NAVER_CLIENT_SECRET,
    }
    req = requests.get(NAVER_REQUEST_URL+"query="+movie_name+"&display=100", headers = header).json()
    req_items = req['items']
    if req_items:
        if director_name:
            for item in req_items:
                check_dir = getDirectorName(item['director'])
                if check_dir == director_name:
                    return item
        return req_items[0]
    else:
        return False

def naverLogin():
    NAVER_ID = os.getenv('NAVER_ID')
    NAVER_PW = os.getenv('NAVER_PW')

    IDxPath='//*[@id="id"]'
    PasswordxPath='//*[@id="pw"]'

    ID=NAVER_ID
    Password=NAVER_PW
    
    copyInput(driver, IDxPath, ID)
    copyInput(driver, PasswordxPath, Password)
    driver.find_element_by_xpath('//*[@value="로그인"]').click()
    time.sleep(1)

def getTrailer(title, s_opt):
    res = ''
    YOUTUBE_KEY = os.getenv('YOUTUBE_KEY')
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
        
def getMovieDetail(movie_code, movie_info, movie_name):
    NAVER_MOVIE_BASE = 'https://movie.naver.com/movie/bi/mi/basic.nhn?code='
    NAVER_IMAGE_URL = 'https://movie.naver.com/movie/bi/mi/photoViewPopup.nhn?movieCode='
    movie_detail_url = NAVER_MOVIE_BASE + movie_code
    driver.get(movie_detail_url)
    time.sleep(1)
    source = driver.page_source          
    soup = BeautifulSoup(source, 'html.parser')
    login_form = soup.find('form', {'id': 'frmNIDLogin'})
    if login_form:
        naverLogin()
        source = driver.page_source          
        soup = BeautifulSoup(source, 'html.parser')

    new_info = {
        'model': 'movies.movie',
        'pk': int(movie_code),
    }
    new_fields = {
        "name": movie_name,
        "name_eng": makeStringFlat(movie_info['subtitle']),
        "watch_grade": "",
        "running_time": "",
        "summary": "",
        "open_date": movie_info['pubDate'],
        "trailer": "",
        "poster": "",
        "directors": [],
        "genres": [],
        "actors": [],
        "score": 0,
    }

    image_url = NAVER_IMAGE_URL+movie_code
    image_html = urllib.request.urlopen(image_url)
    image_soup = BeautifulSoup(image_html, 'lxml')
    image_tag = image_soup.find('img', {'id': 'targetImage'})
    
    if image_tag:
        image_src = image_tag.get('src')
        new_fields['poster'] = image_src
    elif movie_info['image']:
        new_fields['poster'] = tg_movie['image']
    else:
        new_fields['poster'] = ""

    movie_info_dl = soup.find('dl', {'class': 'info_spec'})
    if movie_info_dl:
        atag_list = movie_info_dl.find_all('a')
        for atag in atag_list:
            atag_href = atag.get('href')
            if atag_href != '#':
                key, value = getHrefInfo(atag_href)
                if key == 'genre':
                    new_fields['genres'].append(int(value))
                elif key == 'open':
                    if len(value) > 4:
                        dash_date = value[:4] + '-' + value[4:6] + '-' + value[6:]
                        new_fields['open_date'] = dash_date
                elif key == 'grade' and not new_fields['watch_grade']:
                    new_fields['watch_grade'] = atag.text
        if getRunTime(movie_info_dl):
            new_fields['running_time'] = getRunTime(movie_info_dl)

    people_area = soup.find('div', {'class': 'people'})
    if people_area:
        people_dict = getPeopleInfo(people_area)
        for k, v in people_dict.items():
            new_fields[k] = v

    description = soup.find('div', {'class': 'story_area'})
    if description:
        new_fields['summary'] = getSummary(description.text)
    
    new_info['trailer'] = getTrailer(movie_name, '예고편')

    new_info['fields'] = new_fields
    return new_info
                
def getHrefInfo(tg_href):
    question_idx = tg_href.index('?')
    equal_idx = tg_href.index('=')
    return tg_href[question_idx+1:equal_idx], tg_href[equal_idx+1:]

def getRunTime(tg_area):
    span_tags = tg_area.find_all('span')
    for span_tag in span_tags:
        span_text = span_tag.text
        if '분' in span_text:
            return span_text

def getPeopleInfo(people_area):
    global people_check
    global new_people
    directors = []
    actors = []
    if people_area:
        people_list = people_area.find_all('li')
        for people in people_list:
            dt_tag = people.find('dt')
            dt_class = dt_tag.get('class')
            a_tag = people.find('a', {'class': 'tx_people'})
            if a_tag:
                a_href = a_tag.get('href')
                people_name = a_tag.get('title')
                people_code_str = getCodeFromURL(a_href)
                people_code = int(people_code_str)
                if dt_class[0] == 'staff_dir':
                    directors.append(people_code)
                elif dt_class[0] == 'staff_main':
                    actors.append(people_code)
                
                if not people_check.get(people_code_str):
                    people_check[people_code_str] = people_name
                    new_people.append({
                        'model': 'movies.people',
                        'pk': people_code,
                        'fields': {
                            'name': people_name
                        }
                    })

    people_dict = {}
    people_dict['directors'] = directors
    people_dict['actors'] = actors

    return people_dict

def getSummary(desc):
    cutpoint = 0
    new_desc = desc
    for idx in range(len(desc)-3):
        if desc[idx:idx+3] == '줄거리':
            cutpoint = idx
            new_desc = new_desc[cutpoint+5:]
            break
    
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
    res = makeStringFlat(res)
    return res

def makeStringFlat(tg_str):
    res = tg_str
    res = res.replace ('\xa0', '')
    res = res.replace('\r', '')
    res = res.replace('&amp', '')
    return res

def renameCGV(tg_str):
    idx = len(tg_str)
    for i in range(idx):
        if tg_str[i] == '(':
            return tg_str[:i]
    return tg_str

def getCompanyDetail(tg_dict):
    BASE_DICT = {
        'CGV': 'http://www.cgv.co.kr/movies/detail-view/?midx=',
        'MEGABOX': 'https://www.megabox.co.kr/movie-detail?rpstMovieNo=',
        'LOTTE':'https://www.lottecinema.co.kr/NLCHS/Movie/MovieDetailView?movie=',
        'YES': 'https://movie.yes24.com/MovieInfo/Index?mId=M'
    }
    director_name = ''
    for company, code in tg_dict.items():
        if company == 'CINEQ':
            return ''

        base_url = BASE_DICT[company]
        detail_url = base_url + code
        detail_html = urllib.request.urlopen(detail_url)
        detail_soup = BeautifulSoup(detail_html, 'lxml')
        if company == 'CGV':
            info_box = detail_soup.find('div', {'class': 'spec'})
            director_name_atag = info_box.find('a')
            if director_name_atag:
                director_name = director_name_atag.text

        elif company == 'MEGABOX':
            driver.get(detail_url)
            time.sleep(2)
            detail_source = driver.page_source          
            detail_soup = BeautifulSoup(detail_source, 'html.parser')
            spec_box = detail_soup.find('div', {'class': 'movie-info infoContent'})
            if spec_box:
                div_line = spec_box.find('div', {'class': 'line'})
                if div_line:
                    director_name = spec_box.find('p')
                    if director_name:
                        director_name = renameMega(director_name.text)
        elif company == 'LOTTE':
            driver.get(detail_url)
            time.sleep(2)
            detail_source = driver.page_source          
            detail_soup = BeautifulSoup(detail_source, 'html.parser')
            ul_box = detail_soup.find('ul', {'class': 'sub_info2'})
            if ul_box and ul_box.find('em').text == '감독':
                director_name = ul_box.find('a').text
        
        elif company == 'YES':
            driver.get(detail_url)
            time.sleep(2)
            detail_source = driver.page_source
            detail_soup = BeautifulSoup(detail_source, 'html.parser')
            people_list = detail_soup.find_all('div', {'class': 'act_info'})
            for people in people_list:
                people_job = people.find('p', {'class': 'job'})
                if people_job and people_job.text == '감독':
                    director_name = people.find('p', {'class': 'name dot_st'}).text
                    break
        if director_name:
            break
    return director_name

def rename(tg_str):
    res = tg_str
    idx = 0
    for i in range(len(res)):
        if tg_str[i] == '@':
            idx = i
            break
    if idx:
        res = res[:idx]
    for i in range(len(res)):
        if res[i] == '+':
            idx = i
    if idx:
        res = res[:idx-1]
    return res

def renameMega(tg_str):
    res = ''
    if tg_str[:2] == '감독':
        end_idx = len(tg_str)
        st_idx = 0
        for i in range(len(tg_str)):
            if tg_str[i] == ':':
                st_idx = i+2
            if tg_str[i] == ',':
                end_idx = i
                break
        return tg_str[st_idx:end_idx]
    else:
        return res


chromedriver_dir=r'C:\Users\multicampus\Downloads\chromedriver\chromedriver.exe'
load_dotenv(verbose=True)

with open('06_complete.json', 'r', encoding='UTF-8') as fr:
    complete_list = json.load(fr)

with open('05_people_save.json', 'r', encoding='UTF-8') as fr:
    people_save = json.load(fr)

with open('04_peoples_save.json', 'r', encoding='UTF-8') as fr:
    people_check = json.load(fr)

new_movie = []
new_people = []
not_found = {
    'pk': 1,
    'model': 'movies.movie',
    'fields': {
            "name": "정보 없음",
            "name_eng": "404 Not Found",
            "watch_grade": "관계자외 출입금지",
            "running_time": "",
            "summary": "영화 정보를 찾지 못하였습니다.\n",
            "open_date": "2019-07-01",
            "trailer": "",
            "poster": "",
            "directors": [],
            "genres": [],
            "actors": []
        }
    }

def matchingMovieCode():
    global driver
    driver = webdriver.Chrome(chromedriver_dir)

    with open('07_movie_dict.json', 'r', encoding='UTF-8') as fr:
        movie_dict = json.load(fr)

    for k, v in movie_dict.items():
        if k[0] == '[':
            movie_name = getMovieName(k)
        elif k[0] == '(':
            movie_name = deleteGwal(k)
        else:
            movie_name = k
        director_name = getCompanyDetail(v)
        movie_name = rename(movie_name)
        naver_info = getNaverInfo(movie_name, director_name)
        if naver_info:
            naver_code = getCodeFromURL(naver_info['link'])
            if complete_list.get(naver_code):
                v['NAVER'] = naver_code
            else:
                new_movie_info = getMovieDetail(naver_code, naver_info, movie_name)
                new_movie.append(new_movie_info)
                complete_list[naver_code] = movie_name
                v['NAVER'] = naver_code
                
        else:
            v['NAVER'] = "1"

    driver.quit()
    new_movie.append(not_found)

    with open('08_new_movie.json', 'w', encoding='UTF-8') as fp:
        json.dump(new_movie, fp, ensure_ascii=False, indent=4)

    with open('08_new_people.json', 'w', encoding='UTF-8') as fp:
        json.dump(new_people, fp, ensure_ascii=False, indent=4)

    with open('08_movie_match.json', 'w', encoding='UTF-8') as fp:
        json.dump(movie_dict, fp, ensure_ascii=False, indent=4)

    with open('06_complete.json', 'w', encoding='UTF-8') as fp:
        json.dump(complete_list, fp, ensure_ascii=False, indent=4)

    with open('04_peoples_save.json', 'w', encoding='UTF-8') as fp:
        json.dump(people_check, fp, ensure_ascii=False, indent=4)
