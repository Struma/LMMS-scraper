#This code pulls shitloads of datas for lmms presets because the internet sucks
#sometimes and nobody wants to download 1000 presets manually. I don't want to
#even try ten.


"""
Some notes about the lmms website
location:https://lmms.io/lsp/
name: LMMS sharing plaform
page style: pages of links with options for search and some filtering

"""

import requests
import os
from bs4 import BeautifulSoup
import re

target_dir = raw_input("give me a target dir")
target_url = 'https://lmms.io/lsp/?action=browse&category=Presets&sort=rating'
main_url = 'https://lmms.io'
php_url = 'https://lmms.io/lsp/download_file.php?'

#get the first page to load up our page and link list
r = requests.get(target_url)
soup = BeautifulSoup(r.content, 'html.parser')

#get all the links to the rest of the pages
pagelinktag = soup.find('ul', "pagination pagination-sm")
pagelinks = [main_url + tag.get('href') for tag in pagelinktag.find_all('a')]

#pagelinks.insert(0, target_url)

for page in pagelinks:
    req = requests.get(page)
    soup = BeautifulSoup(req.content, 'html.parser')
    x = soup.find_all('tr')
    links = [tag.find_next('a').get('href') for tag in x]

    links2 =[(main_url + link) for link in links]

    for link in links2:
        requ = requests.get(link)
        t_soup  = BeautifulSoup(requ.content, "html.parser")
        tags = [x for x in t_soup.find_all('a', 'lsp-dl-btn btn btn-primary')]
        for tag in tags:
            dlink = tag.get('href')
            regex = r'(?<!^file=)(\d+\d)(?:&name=)(.*)'
            w = re.search(regex, dlink)
            dlink = main_url +'/lsp/' + dlink
            #payload = {'file': w.group(1),'name': w.group(2)}

            try:
                downpage = requests.get(dlink, allow_redirects = True)
                print("worked")
                with open(( w.group(2)), 'wb') as f:
                    f.write(downpage.content)
                f.close()
            except:
                print('File Failed to Download, WTF -.-')

