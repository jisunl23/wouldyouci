from bs4 import BeautifulSoup
import urllib.request
from datetime import datetime, timedelta
from dotenv import load_dotenv
import json

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

with open('01_movie_list.json', 'r', encoding='UTF-8-sig') as fr:
    movie_list = json.load(fr)

def getMovieCode(tg_str):
    fr_idx = 0
    to_idx = 0
    for i in range(len(tg_str)):
        s = tg_str[i]
        if s == '&':
            if fr_idx == 0:
                fr_idx = i+7
            else:
                to_idx = i
    return tg_str[fr_idx:to_idx]


def getComment(rv):
    idx_list = []
    for idx in range(len(rv)):
        if rv[idx] == ',':
            idx_list.append(idx)

    start_idx = idx_list[1] + 3
    end_idx = idx_list[-2] -1
    res = rv[start_idx:end_idx]

    amp_list = []
    for idx in range(len(res)-4):
        if res[idx:idx+4] == '&amp':
            amp_list.append(idx)
    if amp_list:
        s_point = 0
        new_res = ''
        for i in amp_list:
            e_point = i+9
            if i+7 < len(res):
                if res[i+7] == ';':
                    e_point = i+8
            else:
                if res[i+4] == ';':
                    e_point = i+5
            new_res += res[s_point:i]
            s_point = e_point
        new_res += res[s_point:]
        res = new_res
    return res

user_dummy = []
review_dummy = []
base_url = 'https://movie.naver.com'
movie_detail_base = '/movie/bi/mi/basic.nhn?code='

chromedriver_dir=r'C:\Users\multicampus\Downloads\chromedriver\chromedriver.exe'
driver = webdriver.Chrome(chromedriver_dir)
d_sign = 9000000
temp_pw = "pbkdf2_sha256$180000$zSy1SfdmlRPA$SrsLo8KA42gajN/1soHgL/j4Y2568HmFcOTYtHVyGvM="
new_movie_list = {}

property_dict = {
    'user_cnt': 0
}

for tg_url, ti in movie_list.items():
    with open('02_completed.json', 'r', encoding='UTF-8-sig') as fr:
        complete_list = json.load(fr)

    with open('02_property_dict_save.json', 'r', encoding='UTF-8-sig') as fr:
        property_dict = json.load(fr)
    user_cnt = property_dict['user_cnt']
    
    if complete_list.get(tg_url):
        continue
    else:
        detail_url = base_url + tg_url
        driver.get(detail_url)
        source = driver.page_source          
        soup = BeautifulSoup(source, 'html.parser')
        if soup.find('div', {'class': 'main_score'}):
            new_movie_list[tg_url] = ti
            complete_list[tg_url] = ti
            reviews = driver.find_elements_by_xpath('//*[@class="score_reple"]/dl/dt/em/a')
            reviews_num = len(reviews)
            for i in range(reviews_num):
                rev = reviews[i]
                rev.click()
                try:
                    new_user = {}
                    new_fields = {}

                    new_user['model'] = 'accounts.user'
                    new_user['pk'] = d_sign + user_cnt

                    new_fields['username'] = 'mrWoo' + str(user_cnt)
                    new_fields['email'] = 'dd@naver.com'
                    new_fields['password'] = temp_pw
                    new_fields['get_agreement'] = True
                    new_fields['is_active'] = True
                    new_fields['is_admin'] = False
                    new_fields['last_login'] = None

                    # review_set = []
                    until_review = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,"author")))
                    source = driver.page_source          
                    soup = BeautifulSoup(source, 'html.parser')
                    user_review_list = soup.find_all('td', {'class': 'title'})
                    review_pk_list = soup.find_all('td', {'class': 'ac num'})
                    review_score_list = soup.find_all('div', {'class': 'list_netizen_score'})
                    for i in range(len(user_review_list)):
                        new_review = {
                            'pk': 0,
                            'model': 'accounts.rating',
                        }
                        new_rv_fields = {}
                        rv = user_review_list[i]
                        rv_id = review_pk_list[i].text
                        new_rv_id = int(str(user_cnt)+rv_id)
                        rv_score = int(review_score_list[i].find('em').text)

                        rv_report = rv.find('a', {'class': 'report'})
                        rv_comment = getComment(rv_report.get('href'))

                        movie_info = rv.find('a', {'class': 'movie color_b'})
                        movie_name = movie_info.text
                        movie_href = movie_info.get('href')
                        movie_code = getMovieCode(movie_href)

                        new_review['pk'] = new_rv_id
                        new_rv_fields['movie'] = int(movie_code)
                        new_rv_fields['score'] = rv_score//2
                        new_rv_fields['user'] = d_sign + user_cnt
                        new_rv_fields['comment'] = rv_comment
                        new_rv_fields['created_at'] = "2020-05-18T06:22:06.570Z"
                        new_rv_fields['updated_at'] = "2020-05-18T06:22:06.570Z"
                        new_review['fields'] = new_rv_fields

                        review_dummy.append(new_review)
                        # review_set.append(new_rv_id)

                        movie_url = movie_detail_base + movie_code
                        new_movie_list[movie_url] = movie_name

                    # new_fields['review_set'] = review_set
                    new_user['fields'] = new_fields
                    user_dummy.append(new_user)

                finally:
                    driver.back()
                    user_cnt += 1
                    until_back = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@class="score_reple"]/dl/dt/em/a')))
                    reviews = driver.find_elements_by_xpath('//*[@class="score_reple"]/dl/dt/em/a')
        
        property_dict['user_cnt'] = user_cnt

        with open('02_completed.json', 'w', encoding='UTF-8') as fp:
            json.dump(complete_list, fp, ensure_ascii=False, indent=4)

        with open('02_users_save.json', 'w', encoding='UTF-8') as fp:
            json.dump(user_dummy, fp, ensure_ascii=False, indent=4)

        with open('02_movie_list_save.json', 'w', encoding='UTF-8') as fp:
            json.dump(new_movie_list, fp, ensure_ascii=False, indent=4)

        with open('02_rating_save.json', 'w', encoding='UTF-8') as fp:
            json.dump(review_dummy, fp, ensure_ascii=False, indent=4)

        with open('02_property_dict_save.json', 'w', encoding='UTF-8') as fp:
            json.dump(property_dict, fp, ensure_ascii=False, indent=4)
        
# driver.quit()

# with open('02_users.json', 'w', encoding='UTF-8') as fp:
#     json.dump(user_dummy, fp, ensure_ascii=False, indent=4)

# with open('02_movie_list.json', 'w', encoding='UTF-8') as fp:
#     json.dump(new_movie_list, fp, ensure_ascii=False, indent=4)

# with open('02_rating.json', 'w', encoding='UTF-8') as fp:
#     json.dump(review_dummy, fp, ensure_ascii=False, indent=4)

# print('*********************끝까지했다!**************************')

# 200514 
# review의 형식도 모델에 맞게 고쳐야한다 > 모델 구성하자
# 이제 여기다가 영화 정보만 가져오면 되겠다

# fixture 보면서 모델이랑 형식 맞추기
# comment 보아하니 있다.. 신고 버튼에 property로 들어가있으니 넣어보도록 하자
