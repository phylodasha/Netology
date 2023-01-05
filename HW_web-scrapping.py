import bs4
import requests
from datetime import timedelta
import datetime
URL = 'https://habr.com/ru/all/'
# определяем список ключевых слов
KEYWORDS = ['2022', '2023', 'сайт', 'python']

# Ваш код
response = requests.get(URL)
text = response.text
soup = bs4.BeautifulSoup(text, features='html.parser')
# articles = soup.find_all(class_='tm-articles-list')
articles = soup.find_all('article')
titles_list = []
dates_list =[]
urls_list = []
today = str(datetime.date.today())
yesterday = str(datetime.date.today() - timedelta(1))

for article in articles:
    title = article.find('h2')
    for word in KEYWORDS:
        if word in title.text.lower():
            date = article.find('time')
            if 'сегодня' in date.text:
                        print(today + ', ' + date.text[-5:], end=' | ')
            elif 'вчера' in date.text:
                        print(yesterday + ', ' + date.text[-5:], end=' | ')
            else:
                        print(date.text, end=' | ')
            print(title.text, end = ' | ')
            urls = article.find_all('a')
            for url in urls:
                if url.get('href') and ('/post' in url.get('href') or '/blog' in url.get('href')):
                    print('https://habr.com'+url.get('href'))
                    break


