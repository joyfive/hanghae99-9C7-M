import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
import certifi

from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

ca = certifi.where()

jclient = MongoClient('mongodb+srv://joyfive:whdlvkdlqm999@cluster0.omhyorx.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
jdb = jclient.dbsparta

# https://www.genie.co.kr/detail/songInfo?xgnm=97582507
# https://www.genie.co.kr/detail/albumInfo?axnm=82842800



# print(img,title,artist)


@app.route('/')
def home():
   return render_template('index.html')

@app.route("/album", methods=["POST"])
def album_input():
    album_receive = request.form["album_give"]

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    params = {'axnm': album_receive}
    res = requests.get('https://www.genie.co.kr/detail/albumInfo', headers=headers, params=params)
    soup = BeautifulSoup(res.text, 'html.parser')
    s_artist = soup.select_one('div.info-zone > ul > li:nth-child(1) > span.value > a')
    s_img = soup.select_one('div.album-detail-infos > div.photo-zone > a > span.cover')
    s_tit = soup.select_one('#body-content > div.album-detail-infos > div.info-zone > h2')

    img = s_img.find('img')['src'][19:-19],
    title = s_tit.text.strip(),
    artist = s_artist.text

    item = {
        'img': img,
        'title': title,
        'artist': artist
    }
    return jsonify({'item': item})

# @app.route("/album", methods=["GET"])
# def album_preview():












if __name__ == '__main__':
    app.run('0.0.0.0', port=5050, debug=True)