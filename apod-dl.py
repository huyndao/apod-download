#!/usr/bin/env python3
import requests
import re
import os
import argparse
import json
from bs4 import BeautifulSoup
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

SAVEDIR = 'apod-images'
if not os.path.exists(SAVEDIR):
    os.makedirs(SAVEDIR, exist_ok=False)

url = "https://apod.nasa.gov/apod/astropix.html"
parenturl = os.path.split(url)[0] 

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0'}
spaceregex = re.compile(r'\s{2,}')

def get_apod(url):
    print(f'getting image from {url}')
    sess = requests.Session()
    apod = sess.get(url, timeout=5, headers=headers, verify=True)
    apod.raise_for_status()

    apodsoup = BeautifulSoup(apod.text, features="lxml")
    apod.close()
    prevlink = parenturl + '/' + apodsoup.find_all('a', string="<")[0].get('href')
    imgelem = apodsoup.select('p a[href^="image"]')

    if imgelem == []:
        print('No image link found\n')
    else:
        imgurl = parenturl + '/' + imgelem[0].get('href')
        imgfilename = os.path.basename(imgurl)
        imgdate = imgelem[0].find_previous('p').getText(strip=True)
        imgtitle = imgelem[0].find_next('b').getText(strip=True)
        imgtext = imgelem[0].find_next('p').getText()
        imgtext = re.sub('\n', ' ', imgtext).strip()
        imgtext = re.sub(spaceregex, ' ', imgtext)

        with open(os.path.join(SAVEDIR, "album_list.txt"), 'at') as albumfd:
            print(f'save album list to {os.path.join(SAVEDIR, "album_list.txt")}')
            albumfd.write(imgdate + ' - ' + imgfilename + ' - ' +  imgtitle + ' - ' + imgtext + '\n\n')
            print(f'{imgurl} --> {os.path.join(SAVEDIR, imgfilename)}')
            if not os.path.exists(os.path.join(SAVEDIR, imgfilename)):
                imageresp = sess.get(imgurl, headers=headers, timeout=5, cookies=apod.cookies, stream=True, verify=True)
                imageresp.raise_for_status()
                with open(os.path.join(SAVEDIR, imgfilename), 'wb') as fd:
                    for chunk in imageresp.iter_content(chunk_size=10*1024):
                        print('.', end='', flush=True)
                        fd.write(chunk)
                    print('\n')
                    fd.flush()
                imageresp.close()
            else:
                print(f'file {imgfilename} already downloaded\n')
            albumfd.flush()

    sess.close()
    return prevlink

if __name__ == '__main__':
    while url:
        url = get_apod(url)

