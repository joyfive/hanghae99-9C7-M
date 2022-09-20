import requests
from bs4 import BeautifulSoup

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

params = {'axnm': 81867444}
res = requests.get('https://www.genie.co.kr/detail/albumInfo', headers=headers, params=params)

# https://www.genie.co.kr/detail/songInfo?xgnm=97582507
# https://www.genie.co.kr/detail/albumInfo?axnm=82842800
soup = BeautifulSoup(res.text, 'html.parser')

s_artist = soup.select_one('div.info-zone > ul > li:nth-child(1) > span.value > a')

s_img = soup.select_one('div.album-detail-infos > div.photo-zone > a > span.cover')
s_tit = soup.select_one('#body-content > div.album-detail-infos > div.info-zone > h2')

img = s_img.find('img')['src'][2:-19]
title = s_tit.text.strip()
artist = s_artist.text


print(img,title,artist)