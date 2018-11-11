from itertools import zip_longest

import requests
from bs4 import BeautifulSoup

base_link_pl = 'http://rjawor.home.amu.edu.pl'
base_link_en = "http://rjawor.home.amu.edu.pl/index_en.php"
frases_pl = []
frases_en = []


def get_frases_from_link(link, lang):
    http = requests.get(base_link_pl + "/" + link)
    soup = BeautifulSoup(http.text, 'html.parser')
    frases = soup.find('div', attrs={'id': 'content'}).find('div', attrs={'id': 'column2'}).find_all('p')
    for idx, f in enumerate(frases):
        for frase in f.text.strip().replace('im. ', 'im.').replace('ul. ', 'ul.').replace('np. ', 'np.').\
                replace('ang. ', 'ang.').replace('m.in. ', 'm.in.').replace('p.t. ', 'p.t.').replace('e.g. ', 'e.g.')\
                .split('. '):
            ix = frase.find("\n")
            if ix > -1:
                fras = frase.split('\n')
                for f in fras:
                    if lang == 0:
                        frases_pl.append(f)
                    else:
                        frases_en.append(f)
                    write_to_file(f, lang)
                continue
            elif frase.find('im.'):
                    frase = frase.replace('im.', 'im. ').replace('ul.', 'ul. ').replace('np.', 'np. ').\
                        replace('ang.', 'ang. ').replace('m.in.', 'm.in. ').replace('p.t.', 'p.t. ').\
                        replace('e.g.', 'e.g. ')
                    if lang == 0:
                        frases_pl.append(frase)
                    else:
                        frases_en.append(frase)
                    write_to_file(frase, lang)


def write_to_file(line, lang):
    if lang == 0:
        f = open("pl.txt", "a", encoding='utf-8')
    else:
        f = open("en.txt", "a", encoding='utf-8')
    f.write(line + "\n")


http = requests.get(base_link_pl)
soup = BeautifulSoup(http.text, 'html.parser')
links = soup.find('div', attrs={'id':'menu'}).find_all('a')
for x in range(len(links)):
    link = links[x].get('href')
    get_frases_from_link(link, 0)

http = requests.get(base_link_en)
soup = BeautifulSoup(http.text, 'html.parser')
links = soup.find('div', attrs={'id':'menu'}).find_all('a')
for x in range(len(links)):
    link = links[x].get('href')
    get_frases_from_link(link, 1)

for ind, (pl, en) in enumerate(zip_longest(frases_pl, frases_en)):
    if pl is not None and en is not None:
        pl = pl.replace("\t", "").replace("  ", "")
        en = en.replace("\t", "").replace("  ", "")
        if str(pl).__len__() == 0 or str(en).__len__() == 0:
            continue
        print('{0} {1:140}   {2}'.format(ind, pl.replace("\t", ""), en.replace("\t", "")))
    elif pl is not None:
        pl = pl.replace("\t", "").replace("  ", "")
        if str(pl).__len__() == 0:
            continue
        print('{0} {1:140}'.format(ind, pl.replace("\t", "")))
    else:
        en = en.replace("\t", "").replace("  ", "")
        if str(en).__len__() == 0:
            continue
        print('{0} {1:140}  {2}'.format(ind, "", en.replace("\t", "")))
