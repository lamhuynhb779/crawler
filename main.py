from bs4 import BeautifulSoup
import urllib.request

url  = 'https://vnexpress.net/'
page = urllib.request.urlopen(url)
soup = BeautifulSoup(page, 'html.parser')

target_class = 'section section_stream_home section_container'

target_content = soup.find('section', class_ = target_class).find('div', class_ = 'container has_border flexbox')
left_news = target_content.find('div', class_ = 'col-left col-small')

articles = left_news.find_all('article')
for article in articles:
    description = article.find('p', class_ = 'description')
    if description:
        title = description.find('a').get('title')
        link  = description.find('a').get('href')
        print('Title: {} - Link: {}'.format(title, link))
        