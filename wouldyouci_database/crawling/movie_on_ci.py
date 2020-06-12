from bs4 import BeautifulSoup
import urllib.request
from dotenv import load_dotenv
import json
import requests
# import pyperclip
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
chromedriver_dir=r'C:\Users\multicampus\Downloads\chromedriver\chromedriver.exe'
load_dotenv(verbose=True)

# CGV INFO
def updateCGV(url_option, tdate, cinema_pk):
    global onscreen_pk
    global onscreen_movie

    CGV_ONSCREEN = []
    tg_date = makeCGVDate(tdate)
    iframe_base = 'http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx?'
    CGV_URL = 'http://www.cgv.co.kr'
    iframe_url = iframe_base + url_option + '&date=' + tg_date
    iframe_html = urllib.request.urlopen(iframe_url)
    soup = BeautifulSoup(iframe_html, 'lxml')
    movie_list = soup.find_all('div', {'class': 'col-times'})

    for movie in movie_list:
        # 영화 정보(영화사 영화 자세히보기 페이지)
        movie_info = movie.find('div', {'class': 'info-movie'})
        movie_atag = movie_info.find('a')
        movie_href = movie_atag.get('href')
        movie_code = getCGVMovieIdx(movie_href)
        movie_name = getCGVMovieName(movie_code)
        if onscreen_movie.get(movie_name):
            onscreen_movie[movie_name]['CGV'] = movie_code
        else:
            onscreen_movie[movie_name] = {
                'CGV': movie_code
            }

        # 상영관 정보
        hall_list = movie.find_all('div', {'class': 'type-hall'})
        for hall in hall_list:
            hall_info = hall.find_all('li')
            movie_d = getCGVStr(hall_info[0].text)
            seat_total = getCGVStr(hall_info[2].text)[1:-1]
            time_table = hall.find('div', {'class': 'info-timetable'})
            atag_list = time_table.find_all('a')
            for atag in atag_list:
                new_onscreen_info = {
                    'pk': onscreen_pk,
                    'model': 'movies.onscreen',
                }
                new_onscreen_info_field = {}
                atag_href = atag.get('href')
                if atag_href == '/':
                    TICKET_URL = CGV_URL + '/ticket/?' + url_option + '&date=' + tg_date
                    seat_left = '준비중'
                    start_time = atag.find('em')
                    start_time = start_time.text
                    end_time = atag.find('span', {'class': 'end-time'}).text
                    end_time = deleteWord(end_time, 3, len(end_time))
                    info_hall = hall.find('div', {'class': 'info-hall'})
                    hall_name = info_hall.find_all('li')[1]
                    hall_name = getCGVStr(hall_name.text)
                else:
                    TICKET_URL = CGV_URL + atag_href
                    start_time = atag.get('data-playstarttime')
                    start_time = makeStrtoTime(start_time)
                    end_time = atag.get('data-playendtime')
                    end_time = makeStrtoTime(end_time)
                    seat_left = atag.get('data-seatremaincnt')
                    hall_name = atag.get('data-screenkorname')
                new_onscreen_info_field['cinema'] = cinema_pk
                new_onscreen_info_field['movie'] = int(movie_code)
                new_onscreen_info_field['cm_code'] = int(movie_code)
                new_onscreen_info_field['date'] = tdate
                new_onscreen_info_field['info'] = movie_d + ' | ' + hall_name
                new_onscreen_info_field['start_time'] = start_time
                new_onscreen_info_field['end_time'] = end_time
                new_onscreen_info_field['total_seats'] = seat_total
                new_onscreen_info_field['seats'] = seat_left
                new_onscreen_info_field['url'] = TICKET_URL
                new_onscreen_info['fields'] = new_onscreen_info_field
                # print(new_onscreen_info)
                CGV_ONSCREEN.append(new_onscreen_info)
                onscreen_pk += 1
    
    return CGV_ONSCREEN
                
def getCGVMovieName(tg_code):
    CGV_MOVIE_DETAIL = 'http://www.cgv.co.kr/movies/detail-view/?midx='
    detail_url = CGV_MOVIE_DETAIL + tg_code
    detail_html = urllib.request.urlopen(detail_url)
    detail_soup = BeautifulSoup(detail_html, 'lxml')
    movie_name = detail_soup.find('div', {'class': 'title'})
    res = movie_name.find('strong').text
    return res


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

def makeStrtoTime(tg_str):
    res = ''
    tg_len = len(tg_str)
    minute = tg_str[tg_len-2:]
    hour = tg_str[:tg_len-2]
    res = hour + ':' + minute
    return res

def deleteWord(tg_str, st_idx, end_idx):
    new_str = tg_str[st_idx:end_idx]
    return new_str

# MEGABOX INFO
def updateMEGABOX(tg_url, tg_date, cinema_pk):
    global onscreen_pk
    global onscreen_movie
    TICKET_BASE = 'https://www.megabox.co.kr/booking/seat?playSchdlNo='
    driver.get(tg_url)
    time.sleep(2)

    # 내일 날짜로 조회
    dotdate = getDotDate(tg_date)
    dayxPath = '//*[@date-data=\"' + dotdate + '\"]'
    tmr_btn = driver.find_element_by_xpath(dayxPath)
    tmr_btn.click()
    time.sleep(2)

    source = driver.page_source          
    soup = BeautifulSoup(source, 'html.parser')
    movie_list = soup.find_all('div', {'class': 'theater-list'})
    MEGABOX_ONSCREEN = []
    for movie_col in movie_list:
        movie_info = movie_col.find('div', {'class': 'theater-tit'})
        movie_name = checkMegaName(movie_info.find_all('p')[1].text)
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
                new_onscreen_info = {
                    'pk': onscreen_pk,
                    'model': 'movies.onscreen',
                }
                new_field = {
                    'cinema': cinema_pk,
                    'movie': '',
                    'date': tg_date,
                    'info': movie_info,
                    'start_time': '',
                    'end_time': '',
                    'total_seats': total_seat,
                    'seats': '',
                    'url': tg_url
                }
                if movie_time.get('play-de') != deleteSlash(tg_date):
                    return []

                if movie_time.get('class') == 'end-time':
                    new_field['start_time'] = movie_time.find('p', {'class': 'time'}).text
                    new_field['seats'] = '매진'
                else:
                    book_code = movie_time.get('play-schdl-no')
                    if book_code:
                        TICKET_URL = TICKET_BASE + book_code
                    else:
                        TICKET_URL = tg_url
                    movie_code = movie_time.get('rpst-movie-no')
                    # 상영작 업로드
                    if movie_name and movie_code:
                        if onscreen_movie.get(movie_name):
                            onscreen_movie[movie_name]['MEGABOX'] = movie_code
                        else:
                            onscreen_movie[movie_name] = {
                                'MEGABOX': movie_code
                            }

                    play_info = movie_time.find('div', {'class': 'play-time'})
                    if play_info:
                        play_time = play_info.find('p').text
                        start_end = divideTime(play_time)
                        seat_left = movie_time.find('p', {'class': 'chair'}).text[:-1]
                        new_field['start_time'] = start_end[0]
                        new_field['end_time'] = start_end[1]
                        new_field['seats'] = seat_left

                    if movie_code:
                        new_field['movie'] = int(movie_code)
                        new_field['cm_code'] = int(movie_code)
                    else:
                        continue
                    
                    new_field['url'] = TICKET_URL
                new_onscreen_info['fields'] = new_field
                MEGABOX_ONSCREEN.append(new_onscreen_info)
                onscreen_pk += 1
    return MEGABOX_ONSCREEN

def getDashDate(tg_date):
    res = tg_date[:4] + '-' + tg_date[4:6] + '-' + tg_date[6:]
    return res

def divideTime(tg_time):
    divideIdx = tg_time.index('~')
    res1 = tg_time[:divideIdx]
    res2 = tg_time[divideIdx+1:]
    return res1, res2
    
def makeCGVDate(tg_date):
    res = ''
    for idx in range(len(tg_date)):
        if tg_date[idx] == '-':
            continue
        else:
            res += tg_date[idx]
    return res

def checkMegaName(tg_str):
    if tg_str[0] == '[':
        endIdx = tg_str.index(']')
        return tg_str[endIdx+2:]
    elif tg_str[0] == '(':
        endIdx = tg_str.index(')')
        return tg_str[endIdx+2:]
    else:
        return tg_str

def getDotDate(tdate):
    res = ''
    for idx in range(len(tdate)):
        if tdate[idx] == '-':
            res += '.'
        else:
            res += tdate[idx]
    return res
    
def updateLOTTE(tg_url, tg_date, cinema_pk):
    global onscreen_pk
    global onscreen_movie
    driver.get(tg_url)

    time.sleep(2)
    ck_source = driver.page_source          
    ck_soup = BeautifulSoup(ck_source, 'html.parser')
    ck_layer = ck_soup.find('div', {'id': 'layerGetPopup'})
    if ck_layer.text:
        popupLayer = driver.find_element_by_id('layerGetPopup')
        ck_btn = popupLayer.find_element_by_class_name('btn_close.btnCloseLayer')
        ck_btn.click()
        time.sleep(1)

    day_list = driver.find_elements_by_class_name('date')

    ck_date = str(int(tg_date[-2:]))
    LOTTE_ONSCREEN = []
    # 내일 날짜로 조회
    for day in day_list:
        day_text = day.find_element_by_tag_name('strong').text
        if day_text == ck_date:
            tg_btn = day.find_element_by_tag_name('label')
            tg_btn.click()
            time.sleep(2)
            break
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
        movie_code = findLotteCode(movie_href)
        if onscreen_movie.get(movie_name):
            onscreen_movie[movie_name]['LOTTE'] = movie_code
        else:
            onscreen_movie[movie_name] = {
                'LOTTE': movie_code
            }
        
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
            end_time_info = time_info.find('div', {'class': 'tooltip'}).text
            end_time = strBeforeSpace(end_time_info)
            seat_info = timetable_info.find('dd', {'class': 'seat'})
            seat_left = seat_info.find('strong').text
            seat_total = strBeforeSpace(seat_info.text)
            hall_info = timetable_info.find('dd', {'class': 'hall'}).text
            new_movie_info = movie_info + ' | ' + hall_info

            new_onscreen_info = {
                'pk': onscreen_pk,
                'model': 'movies.onscreen',
                'fields': {
                    'cinema': cinema_pk,
                    'movie': int(movie_code),
                    'date': tg_date,
                    'info': new_movie_info,
                    'start_time': start_time,
                    'end_time': end_time,
                    'total_seats': seat_total,
                    'seats': seat_left,
                    'url': tg_url,
                    'cm_code': int(movie_code)
                }
            }
            onscreen_pk += 1
            LOTTE_ONSCREEN.append(new_onscreen_info)
    return LOTTE_ONSCREEN
            

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

def updateETC(tg_url, tg_date, cinema_pk):
    global onscreen_pk
    global onscreen_movie

    if cinema_pk == 75 or cinema_pk == 84:
        driver.get(tg_url)
        time.sleep(3)

        # 내일 찾기
        tommorow_btn = driver.find_element_by_xpath('//*[@id="content"]/div[2]/div/div[1]/ul/li[3]/a')
        tommorow_btn.click()
        time.sleep(1)

        source = driver.page_source          
        soup = BeautifulSoup(source, 'html.parser')
        time_box = soup.find('div', {'class': 'theater-movie'})
        movie_list = time_box.find_all('div', {'class': 'each-movie-time'})
        CINEQ_ONSCREEN = []
        for movie_div in movie_list:
            movie_title = movie_div.find('div', {'class': 'title'})
            movie_grade = movie_title.find('span').get('class')
            movie_name = getMovieName(movie_title.text, movie_grade[0])
            hall_list = movie_div.find_all('div', {'class': 'screen'})
            for hall in hall_list:
                hall_name = hall.find('div', {'class': 'screen-name'})
                hall_info = hall_name.text
                time_div = hall.find('div', {'class': 'time-block'})
                time_list = time_div.find_all('div', {'class': 'time'})
                for time_info in time_list:
                    movie_code = time_info.get('data-moviecode')
                    if not movie_code:
                        continue
                    else:
                        if onscreen_movie.get(movie_name):
                            onscreen_movie[movie_name]['CINEQ'] = str(int(movie_code))
                        else:
                            onscreen_movie[movie_name] = {
                                'CINEQ': str(int(movie_code))
                            }
                    end_time = time_info.find('span', {'class': 'to'}).text[3:]
                    seat_info = time_info.find('span', {'class': 'seats-status'}).text
                    seat_left, seat_total = getSeatInfo(seat_info)
                    start_text = time_info.find('a').text
                    start_time = getCineqTime(start_text)
                    new_onscreen_info = {
                        'pk': onscreen_pk,
                        'model': 'movies.onscreen',
                        'fields': {
                            'cinema': cinema_pk,
                            'movie': int(movie_code),
                            'date': tg_date,
                            'info': hall_info,
                            'start_time': start_time,
                            'end_time': end_time,
                            'total_seats': seat_total,
                            'seats': seat_left,
                            'url': tg_url,
                            'cm_code': int(movie_code)
                        }
                    }
                    onscreen_pk += 1
                    CINEQ_ONSCREEN.append(new_onscreen_info)
        return CINEQ_ONSCREEN                

    else:
        def getHallInfo(tg_str):
            res1 = ''
            res2 = ''
            for i in range(len(tg_str)):
                if tg_str[i] == '관' and res1 == '':
                    res1 = tg_str[:i+1]
                elif tg_str[i] == ' ' and res2 == '':
                    res2 = tg_str[i+1:]
                    return res1, res2



        def getEndTime(tg_str):
            res = ''
            for i in range(len(tg_str)):
                if tg_str[i] == '~':
                    res = tg_str[i+2:]
                    break
            return res

        def renameYesTitle(tg_str):
            res = tg_str
            if res[len(tg_str)-1] == ')':
                idx = res.index('(')
                res = res[:idx-1]
            if res[0] == '[':
                idx = res.index(']')
                res = res[idx+2:]
            return res

        TICKET_BASE = 'https://movie.yes24.com/Movie/Ticket?gId=&'
        YES_ONSCREEN = []
        driver.get(tg_url)
        until_time = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME,"time_sel_cont")))
        time.sleep(2)
        source = driver.page_source          
        soup = BeautifulSoup(source, 'html.parser')
        if not soup.find('div', {'class': 'show_time_slide'}):
            return []
        # 다음날 버튼 클릭
        ck = True
        tg_day = str(int(tg_date[-2:]))
        day_list = driver.find_elements_by_class_name('show_time_slide')
        for day in day_list:
            span_text = day.find_element_by_tag_name('span').text
            if span_text == tg_day:
                ck = False
                day.click()
                time.sleep(1)
                source = driver.page_source          
                soup = BeautifulSoup(source, 'html.parser')
                break
        if ck:
            return []

        time_container = soup.find('div', {'class': 'time_sel_cont'})
        title_list = time_container.find_all('div', {'class': 'tit'})
        time_list = time_container.find_all('ul', {'class': 'time_sel_list'})
        if len(title_list) == 0:
            return []
        for idx in range(len(title_list)):
            title = title_list[idx]
            title_text = title.text
            hall_info, movie_title = getHallInfo(title_text)
            movie_name = renameYesTitle(movie_title)
            timetable = time_list[idx]
            li_list = timetable.find_all('li')
            for li in li_list:
                atag = li.find('a', {'class': 'time_info_box'})
                pdate = atag.get('playdate')
                if pdate == tg_date:
                    reserve_option = {
                        "mId" : atag.get('mid'),
                        "tId" : atag.get('tid'),
                        "playDate": deleteSlash(tg_date),
                        "pno": atag.get('ptid'),
                    }
                    movie_code = reserve_option['mId'][1:]
                    if onscreen_movie.get(movie_name):
                        onscreen_movie[movie_name]['YES'] = movie_code
                    else:
                        onscreen_movie[movie_name] = {
                            'YES': movie_code
                        }
                    book_option = urllib.parse.urlencode(reserve_option)
                    movie_url = TICKET_BASE + book_option
                    time_info = atag.find('div', {'class': 'time_info'})
                    start_time = time_info.find('div', {'class': 'time_start'}).text
                    playing_time = time_info.find('div', {'class': 'running_time'}).text
                    end_time = getEndTime(playing_time)
                    new_onscreen_info = {
                        'pk': onscreen_pk,
                        'model': 'movies.onscreen',
                        'fields': {
                            'cinema': cinema_pk,
                            'movie': int(movie_code),
                            'date': tg_date,
                            'info': hall_info,
                            'start_time': start_time,
                            'end_time': end_time,
                            'total_seats': '',
                            'seats': '',
                            'url': movie_url,
                            'cm_code': int(movie_code)
                        }
                    }
                    onscreen_pk += 1
                    YES_ONSCREEN.append(new_onscreen_info)
        return YES_ONSCREEN

def getCineqTime(tg_str):
    res = ''
    ck = False
    for i in range(len(tg_str)):
        if tg_str[i] == ' ':
            continue
        elif tg_str[i] == '\n':
            continue
        elif tg_str[i] == ':':
            ck = True
            res += tg_str[i]
        else:
            if not ck:
                res += tg_str[i]
            else:
                res += tg_str[i: i+2]
                break
    if len(res) < 5:
        res = '0' + res
    return res
                
def getSeatInfo(tg_str):
    for i in range(len(tg_str)):
        if tg_str[i] == '/':
            return tg_str[:i-1], tg_str[i+2:]
    return '', ''


def getMovieName(tg_title, tg_grade):
    start_idx = 2
    if tg_grade == 'rate-all':
        start_idx = 1
    res = tg_title[start_idx:-1]
    if res[len(res)-1] == ')':
        end_idx = res.index('(') -1
        res = res[:end_idx]
    return res

def deleteSlash(tg_str):
    res = ''
    for i in range(len(tg_str)):
        if tg_str[i] == '-':
            continue
        else:
            res += tg_str[i]
    return res

today = datetime.date.today()
tr = today + datetime.timedelta(days=1)
tommorow = tr.strftime('%Y-%m-%d')

change_time = {
    "24": "00",
    "25": "01",
    "26": "02",
    "27": "03",
    "28": "04",
    "29": "05",
    "30": "06"
}

onscreen_pk = int(tr.strftime('%Y%m%d0001')[2:])
def getScreenInfo():
    global cinemas
    global on_screen
    global onscreen_movie
    global driver
    
    with open('cinemas.json', 'r', encoding='UTF-8-sig') as fr:
        cinemas = json.load(fr)

    with open('07_on_screen_today.json', 'r', encoding='UTF-8') as fr:
        on_screen = json.load(fr)

    with open('07_movie_dict_today.json', 'r', encoding='UTF-8') as fr:
        onscreen_movie = json.load(fr)
        
    driver = webdriver.Chrome(chromedriver_dir)
    for cinema in cinemas:
        base_url = cinema['fields']['url']
        company = cinema['fields']['type']
        new_on_screen = []

        if company == 'CGV':
            base_url_info = urllib.parse.urlsplit(base_url).query
            new_on_screen = updateCGV(base_url_info, tommorow, cinema['pk'])

        elif company == '메가박스':
            new_on_screen = updateMEGABOX(base_url, tommorow, cinema['pk'])
            
        elif company == '롯데시네마':
            new_on_screen = updateLOTTE(base_url, tommorow, cinema['pk'])

        else:
            new_on_screen = updateETC(base_url, tommorow, cinema['pk'])


        if new_on_screen:
            for screen_info in new_on_screen:
                for t in ['start_time', 'end_time']:
                    movie_time = screen_info['fields'][t]
                    if movie_time:
                        movie_hour = movie_time[:2]
                        if change_time.get(movie_hour):
                            screen_info['fields'][t] = change_time[movie_hour] + movie_time[2:]
                    # else:
                    #     screen_info['fields'][t] = ''
                on_screen.append(screen_info)
        
    driver.quit()

    with open('07_on_screen.json', 'w', encoding='UTF-8') as fp:
        json.dump(on_screen, fp, ensure_ascii=False, indent=4)

    with open('07_movie_dict.json', 'w', encoding='UTF-8') as fp:
        json.dump(onscreen_movie, fp, ensure_ascii=False, indent=4)