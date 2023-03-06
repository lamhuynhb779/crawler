from bs4 import BeautifulSoup
import urllib.request
import re, os

domain = 'https://en.kancollewiki.net'
uri = '/Graf_Zeppelin'
page = urllib.request.urlopen(domain + uri)
soup = BeautifulSoup(page, 'html.parser')

def getCardURL(card_info):
    try:
        card_image  = card_info.find('img')
        srcset      = card_image.get('srcset')
        data        = re.findall(r'\S+', srcset)
        return data[0]
    except Exception as err:
        # print(card_info)
        # raise
        return None

def getCardName(card_info):
    if card_info.get('title') != None:
        return card_info.get('title')
    return None

def selectTargetContent():
    target_content = soup.find('div', class_ = 'mw-body').find('div', attrs={'id': 'bodyContent'})
    all_contents = target_content.find('div', attrs={'id': 'mw-content-text'}).find('div', attrs={'class': 'mw-parser-output'})
    return all_contents.find_all('div', attrs={'style': 'display:inline-block;vertical-align:top'})

def saveFromUrl(url, name):
    cwd = os.getcwd()
    if cwd != '/var/www/crawler/cards':
        os.chdir("cards/")
    urllib.request.urlretrieve(url, f'{name}.png')

def crawShips():
    infos = selectTargetContent()
    for info in infos:
        card_infos = info.find('table').find('tbody').find_all('tr')
        print(card_infos)
        # i = 0
        # for card_info in card_infos:
        #     card_name = getCardName(card_info)

        #     card_url = None

        #     if card_name != None:
        #         card_url = getCardURL(card_info)
        #         saveFromUrl(card_url, card_name)

        #     print('card_name: {}, card_url: {}'.format(card_name, card_url))

crawShips()