import json

with open('04_movies_save.json', 'r', encoding='UTF-8') as fr:
    movies = json.load(fr)

with open('04_notfound_save.json', 'r', encoding='UTF-8') as fr:
    not_found = json.load(fr)

with open('02_rating_save.json', 'r', encoding='UTF-8') as fr:
    ratings = json.load(fr)

new_rating = []
new_movies = []
complete = {}

for movie in movies:
    if not_found.get(str(movie['pk'])):
        continue
    else:
        new_movies.append(movie)
        complete[movie['pk']] = movie['fields']['name']

for rating in ratings:
    if not_found.get(str(rating['fields']['movie'])):
        continue
    else:
        new_rating.append(rating)



with open('06_rating.json', 'w', encoding='UTF-8') as fp:
    json.dump(new_rating, fp, ensure_ascii=False, indent=4)

with open('06_movie.json', 'w', encoding='UTF-8') as fp:
    json.dump(new_movies, fp, ensure_ascii=False, indent=4)

with open('06_complete.json', 'w', encoding='UTF-8') as fp:
    json.dump(complete, fp, ensure_ascii=False, indent=4)