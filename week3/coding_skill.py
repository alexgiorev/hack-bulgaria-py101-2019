import json
import sys

def get_result(data):
    max_level_so_far = {}
    result = {}
    for fullname, langs_levels in form_people(data):
        for language, level in langs_levels:
            if level > max_level_so_far.get(language, 0):
                max_level_so_far[language] = level
                result[language] = fullname
    return result
        
def form_people(data):
    out = []
    for person in data['people']:
        fullname = f'{person["first_name"]} {person["last_name"]}'
        langs_levels = [(skill['name'], skill['level']) for skill in person['skills']]
        out.append((fullname, langs_levels))
    return out
        
filename = sys.argv[1]
with open(filename) as f:
    data = json.loads(f.read())

for lang, name in get_result(data).items():
    print(f'{lang} - {name}')
