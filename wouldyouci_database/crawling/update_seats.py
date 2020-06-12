import pymysql.cursors
from bs4 import BeautifulSoup
import urllib.request
from dotenv import load_dotenv
import json
import requests
import time
import datetime

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

# selenium

today = datetime.date.today()
tg_date = today.strftime('%Y-%m-%d')

load_dotenv(verbose=True)
SQL_INFO = {
    'HOST': os.getenv('HOST'),
    'USER': os.getenv('USER'),
    'PW': os.getenv('PASSWORD'),
    'DB': os.getenv('DB'),
    'PORT': 3306
}

def updateSeats(cinema_pk, cm_code, start_time, seat_total, hall_info, seats):
    global tg_date
    global cursor
    global not_found
    sql_base = "SELECT *  FROM movies_onscreen WHERE "
    sql_option = 'cinema_id = ' + str(cinema_pk) + ' AND date = \"' + tg_date + '\"' + ' AND start_time = \"' + start_time + '\"'  + ' AND cm_code = ' + str(cm_code) + ' AND total_seats = \"' + seat_total + '\"'
    sql = sql_base + sql_option
    cursor.execute(sql)
    rows = cursor.fetchall()
    if rows:
        if len(rows) == 1:
            tg_row = rows[0]
        else:
            for idx in range(len(rows)):
                if rows[idx]['info'] == hall_info:
                    tg_row = rows[idx]
                    break
        tg_idx = tg_row['id']
        tg_total = tg_row['total_seats']
        if int(tg_total) >= int(seats): 
            if tg_row['seats'] != seats:
                update_sql = 'UPDATE wouldyouci.movies_onscreen SET seats = ' + '\"' + seats + '\"' + ' WHERE id = ' + str(tg_idx) + ';'
                cursor.execute(update_sql)
                conn.commit()
        # else:
        #     print('자리 잘못찾음', seats, tg_total, tg_idx)
                
    else:
        not_found.append(sql)

def cinemaLoop():
    global SQL_INFO
    global cursor
    global conn
    global not_found

    with open('cinemas.json', 'r', encoding='UTF-8-sig') as fr:
        cinema_list = json.load(fr)
    
    conn = pymysql.connect(host=SQL_INFO['HOST'], port=SQL_INFO['PORT'], user=SQL_INFO['USER'], password=SQL_INFO['PW'], db=SQL_INFO['DB'], charset='utf8mb4')
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    chromedriver_dir=r'C:\Users\multicampus\Downloads\chromedriver\chromedriver.exe'
    driver = webdriver.Chrome(chromedriver_dir)

    not_found = []
    for cinema in cinema_list:
        company = cinema['fields']['type']
        if company == 'CGV':
            updateCGV(cinema)
        elif company == '메가박스':
            updateMEGABOX(cinema, driver)
        elif company == '롯데시네마':
            updateLOTTE(cinema, driver)

    conn.close()
    driver.quit()
    with open('10_seat_notfound.json', 'w', encoding='UTF-8') as fp:
        json.dump(not_found, fp, ensure_ascii=False, indent=4)

def updateCGV(cinema_info):
    global today

    def getCGVStr(tg_text):
        start_point = 0
        tg_text_len = len(tg_text)
        res = ''
        for idx in range(tg_text_len):
            if tg_text[idx] == ' ':
                continue
            elif tg_text[idx] == '\r':
                continue
            elif tg_text[idx] == '\n':
                continue
            else:
                res += tg_text[idx]
        return res
    
    def getCGVMovieIdx(movie_url):
        equal_idx = movie_url.index('=')
        cgv_movie_code = movie_url[equal_idx+1:]
        return cgv_movie_code

    cinema_pk = cinema_info['pk']
    # change_point
    date_str = today.strftime('%Y%m%d')
    base_url = cinema_info['fields']['url']
    url_option = urllib.parse.urlsplit(base_url).query

    iframe_base = 'http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx?'
    iframe_url = iframe_base + url_option + '&date=' + date_str
    iframe_html = urllib.request.urlopen(iframe_url)
    soup = BeautifulSoup(iframe_html, 'lxml')
    movie_list = soup.find_all('div', {'class': 'col-times'})

    for movie in movie_list:
        movie_info = movie.find('div', {'class': 'info-movie'})
        movie_atag = movie_info.find('a')
        movie_href = movie_atag.get('href')
        movie_code = getCGVMovieIdx(movie_href)
        hall_list = movie.find_all('div', {'class': 'type-hall'})
        for hall in hall_list:
            hall_info = hall.find_all('li')
            movie_d = getCGVStr(hall_info[0].text)
            seat_total = getCGVStr(hall_info[2].text)[1:-1]
            time_table = hall.find('div', {'class': 'info-timetable'})
            atag_list = time_table.find_all('a')
            for atag in atag_list:
                atag_href = atag.get('href')
                if atag_href == '/':
                    seat_left = '0'
                    start_time = atag.find('em')
                    start_time = start_time.text
                    info_hall = hall.find('div', {'class': 'info-hall'})
                    hall_name = info_hall.find_all('li')[1]
                    hall_name = getCGVStr(hall_name.text)
                else:
                    start_time = atag.get('data-playstarttime')
                    start_time = makeStrtoTime(start_time)
                    seat_left = atag.get('data-seatremaincnt')
                    hall_name = atag.get('data-screenkorname')
                hall_info = movie_d + ' | ' + hall_name
                updateSeats(cinema_pk, int(movie_code), start_time, seat_total, hall_info, seat_left)

def updateMEGABOX(cinema_info, driver):
    def divideTime(tg_time):
        divideIdx = tg_time.index('~')
        res1 = tg_time[:divideIdx]
        res2 = tg_time[divideIdx+1:]
        return res1, res2
    cinema_pk = cinema_info['pk']
    tg_url = cinema_info['fields']['url']
    driver.get(tg_url)
    time.sleep(1)
    source = driver.page_source          
    soup = BeautifulSoup(source, 'html.parser')
    movie_list = soup.find_all('div', {'class': 'theater-list'})
    for movie_col in movie_list:
        theater_type_list = movie_col.find_all('div', {'class': 'theater-type-box'})
        for box in theater_type_list:
            theater_type = box.find('div', {'class': 'theater-type'})
            hall_name = theater_type.find('p', {'class': 'theater-name'}).text
            total_seat = theater_type.find('p', {'class': 'chair'}).text[2:-1]
            theater_time = box.find('div', {'class': 'theater-time'})
            movie_d = theater_time.find('div', {'class': 'theater-type-area'}).text
            movie_info = movie_d + ' | ' + hall_name
            movie_timetable = theater_time.find_all('td')
            for movie_time in movie_timetable:
                if movie_time.get('class') == 'end-time':
                    continue
                else:
                    book_code = movie_time.get('play-schdl-no')
                    movie_code = movie_time.get('rpst-movie-no')
                    play_info = movie_time.find('div', {'class': 'play-time'})
                    if movie_code:
                        cm_code = int(movie_code)
                        if play_info:
                            play_time = play_info.find('p').text
                            start_end = divideTime(play_time)
                            seat_left = movie_time.find('p', {'class': 'chair'}).text[:-1]
                            start_time = start_end[0]
                            updateSeats(cinema_pk, cm_code, start_time, total_seat, movie_info, seat_left)


def updateLOTTE(cinema_info, driver):
    def findLotteCode(tg_href):
        idx = 0
        for i in range(len(tg_href)):
            if tg_href[i] == '=':
                idx = i
                break
        if idx:
            return tg_href[idx+1:]

    def strBeforeSpace(tg_str):
        idx = 0
        for i in range(len(tg_str)-1, -1, -1):
            if tg_str[i] == ' ':
                idx = i+1
                break
        return tg_str[idx:]

    cinema_pk = cinema_info['pk']
    tg_url = cinema_info['fields']['url']
    driver.get(tg_url)
    time.sleep(1)

    source = driver.page_source          
    soup = BeautifulSoup(source, 'html.parser')
    # 팝업창이 뜬 경우
    ck_layer = soup.find('div', {'id': 'layerGetPopup'})
    if ck_layer.text:
        popupLayer = driver.find_element_by_id('layerGetPopup')
        ck_btn = popupLayer.find_element_by_class_name('btn_close.btnCloseLayer')
        ck_btn.click()
        time.sleep(1)
        source = driver.page_source          
        soup = BeautifulSoup(source, 'html.parser')

    movie_list = soup.find_all('div', {'class': 'time_select_wrap ty2 timeSelect'})
    for movie in movie_list:
        movie_tit = movie.find('div', {'class': 'list_tit'})
        movie_name = movie_tit.find('p').text
        if movie_name == '테스트콘텐츠':
            continue
        movie_atag = movie_tit.find('a')
        movie_href = movie_atag.get('href')
        cm_code = findLotteCode(movie_href)
        movie_info_ul = movie.find('ul', {'class': 'list_hall mt20'})
        movie_info_li = movie_info_ul.find_all('li')
        movie_info_list = []
        for info_li in movie_info_li:
            movie_info_list.append(info_li.text)
        movie_info = ' | '.join(movie_info_list)
        timetable_ul = movie.find('ul', {'class': 'list_time'})
        timetable_atag_list = timetable_ul.find_all('li')
        for timetable_info in timetable_atag_list:
            time_info = timetable_info.find('dd', {'class': 'time'})
            start_time = time_info.find('strong').text
            seat_info = timetable_info.find('dd', {'class': 'seat'})
            seat_left = seat_info.find('strong').text
            if seat_left == '예매마감':
                continue
            seat_total = strBeforeSpace(seat_info.text)
            hall_info = timetable_info.find('dd', {'class': 'hall'}).text
            new_movie_info = movie_info + ' | ' + hall_info
            updateSeats(cinema_pk, cm_code, start_time, seat_total, new_movie_info, seat_left)


def makeStrtoTime(tg_str):
    res = ''
    tg_len = len(tg_str)
    minute = tg_str[tg_len-2:]
    hour = tg_str[:tg_len-2]
    res = hour + ':' + minute
    return res

# python_start = time.time()

# print('****************************** 작업완료! *************************************')
# print( time.time() - python_start )