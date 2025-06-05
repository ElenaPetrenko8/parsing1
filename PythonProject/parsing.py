import requests
from bs4 import BeautifulSoup


def collect_user_rates(user_login):
    page_num = 1
    data = []

    while True:
        url = f'https://letterboxd.com/{user_login}/films/diary/page/{page_num}/'
        response = requests.get(url)
        if response.status_code != 200:
            
            break
        html_content = response.text
        soup = BeautifulSoup(html_content, 'lxml')

        entries = soup.find_all('tr', class_='diary-entry-row viewing-poster-container')
        if not entries:
            break

        for entry in entries:
            td_film_details = entry.find('td', class_='td-film-details')
            if not td_film_details:
                continue
            film_name_tag = td_film_details.find('a')
            if not film_name_tag:
                continue
            film_name = film_name_tag.text.strip()

            release_date_tag = entry.find('td', class_='td-released center')
            release_date = release_date_tag.text.strip() if release_date_tag else ''

            td_rating_rating_green = entry.find('td', class_='td-rating rating-green')
            rating_span = td_rating_rating_green.find('span', class_='rating') if td_rating_rating_green else None
            classes = rating_span.get('class', []) if rating_span else []

            
            rating_class = classes[1] if len(classes) > 1 else ''
            rating_parts = rating_class.split('-')
            rating_value = int(rating_parts[1]) if len(rating_parts) > 1 and rating_parts[1].isdigit() else 0

            data.append({
                'film_name': film_name,
                'release_date': release_date,
                'rating': rating_value
            })

        page_num += 1

    return data


user_login_input = 'rfeldman9'  # заменить на нужный логин


user_rates = collect_user_rates(user_login=user_login_input)


films_2024 = [film for film in user_rates if '2024' in film['release_date']]


top_5_films_2024 = sorted(films_2024, key=lambda x: x['rating'], reverse=True)[:5]


for idx, film in enumerate(top_5_films_2024, start=1):
    print(f"{idx}. {film['film_name']} ({film['release_date']}) - Рейтинг: {film['rating']}")

import requests
from bs4 import BeautifulSoup

import pandas as pd

def collect_user_rates(user_login): ...


user_rates = collect_user_rates(user_login='rfeldman9')
df = pd.DataFrame(user_rates)

df.to_excel('user_rates2.xlsx')
