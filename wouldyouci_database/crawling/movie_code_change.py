import json

def findCinemaCompany(tg_pk):
    if tg_pk == 75 or tg_pk == 84:
        return 'CINEQ'
    elif tg_pk == 74 or (tg_pk > 75 and tg_pk != 84):
        return 'YES'

    for cinema in cinema_list:
        if cinema['pk'] == tg_pk:
            company = cinema['fields']['type']
            if company == '롯데시네마':
                company = 'LOTTE'
            elif company == '메가박스':
                company = 'MEGABOX'
            return company
        
def getNaverCode(tg_code, company):
    for k, v in code_dict.items():
        if v.get(company):
            if int(v[company]) == int(tg_code):
                return v.get('NAVER')

def movieCodeChange():
    global cinema_list
    global code_dict
    with open('07_on_screen.json', 'r', encoding='UTF-8') as fr:
        on_screen = json.load(fr)

    with open('08_movie_match.json', 'r', encoding='UTF-8') as fr:
        code_dict = json.load(fr)

    with open('cinemas.json', 'r', encoding='UTF-8-sig') as fr:
        cinema_list = json.load(fr)

    for movie in on_screen:
        compnay_movie_code = str(movie['fields']['movie'])
        cinema_pk = movie['fields']['cinema']
        cinema_company = findCinemaCompany(cinema_pk)
        naver_code = getNaverCode(compnay_movie_code, cinema_company)
        if naver_code:
            movie['fields']['movie'] = int(naver_code)
        else:
            movie['fields']['movie'] = 1

    with open('09_onscreen.json', 'w', encoding='UTF-8') as fp:
        json.dump(on_screen, fp, ensure_ascii=False, indent=4)