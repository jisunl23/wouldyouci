import json

with open('04_peoples_save.json', 'r', encoding='UTF-8') as fr:
    people_list = json.load(fr)


people_dict = []
for k, v in people_list.items():
    new_people = {
        'model': 'movies.people',
        'pk': int(k),
        'fields': {
            'name': v
        }
    }
    people_dict.append(new_people)
with open('05_people_save.json', 'w', encoding='UTF-8') as fp:
    json.dump(people_dict, fp, ensure_ascii=False, indent=4)