import sys
import json

def html_dict_to_text(html_dict):
    tag = html_dict['tag']
    attributes = html_dict['attributes']
    children = html_dict['children']

    attributes_str = ' '.join(f'{name}="{value}"' for name, value in attributes.items())
    if children:
        children_str = ' '.join(child if type(child) is str else html_dict_to_text(child)
                                for child in children)
        return f'<{tag} {attributes_str}>{children_str}</{tag}>'
    else:
        return f'<{tag} {attributes_str}>'

def make_html_dict(tag, attributes, *children):
    return {'tag': tag, 'attributes': attributes, 'children': children}
    
def person_fullname(person):
    return f'{person["first_name"]} {person["last_name"]}'

def person_to_html(person):
    return html_dict_to_text(person_to_business_card_html_dict(person))

def person_html_filename(person):
    return f'{person["first_name"].lower()}_{person["last_name"].lower()}.html'

def person_to_business_card_html_dict(person):
    # returns the html dict that when parsed into html
    # will represent the business card of @person

    def interests_list():
        items = [make_html_dict('li', {}, interest) for interest in person['interests']]
        return make_html_dict('ul', {}, *items)

    def skills_list():
        items = [make_html_dict('li', {}, f'{skill["name"]} - {skill["level"]}') for skill in person['skills']]
        return make_html_dict('ul', {}, *items)
    
    head_title = make_html_dict('title', {}, person_fullname(person))
    head_link = make_html_dict('link', {'rel': 'stylesheet', 'type': 'text/css', 'href': 'styles.css'})
    head = make_html_dict('head', {}, head_title, head_link)
    header = make_html_dict('h1', {'class': 'full-name'}, person_fullname(person))
    avatar = make_html_dict('img', {'class': 'avatar', 'src': f'avatars/{person["avatar"]}'})
    age = make_html_dict('p', {}, f'Age: {person["age"]}')
    birth_day = make_html_dict('p', {}, f'Birth date: {person["birth_date"]}')
    birth_place = make_html_dict('p', {}, f'Birth place: {person["birth_place"]}')
    gender = make_html_dict('p', {}, f'Gender: {person["gender"]}')
    base_info = make_html_dict('div', {'class': 'base-info'}, age, birth_day, birth_place, gender)
    interests_header = make_html_dict('h2', {}, 'Interests:')
    interests = make_html_dict('div', {'class': 'interests'}, interests_header, interests_list())
    skills_header = make_html_dict('h2', {}, 'Skills:')
    skills = make_html_dict('div', {'class': 'skills'}, skills_header, skills_list())
    body_div = make_html_dict('div', {'class': f'business-card {person["gender"]}'},
                              header, avatar, base_info, interests, skills)
    body = make_html_dict('body', {}, body_div)
    html = make_html_dict('html', {}, head, body)
    return html

def main(filename, directory):
    with open(filename) as f:
        data = json.loads(f.read())
        
    filenames = []
    for person in data['people']:
        new_filename = f'{directory}/{person_html_filename(person)}'
        html_text = person_to_html(person)
        with open(new_filename, 'w') as f:
            f.write(html_text)
        filenames.append(new_filename)
    return filenames

if __name__ == '__main__':
     filename = sys.argv[1]
     if len(sys.argv) == 2:
         directory = '.'
     else:
         directory = sys.argv[2]
     print('\n'.join(main(filename, directory)))

