from flask import Flask, render_template, request, jsonify
from bs4 import BeautifulSoup
import requests
from secretkey import secret_key
app = Flask(__name__)

from pymongo import MongoClient
import certifi

ca = certifi.where()
SECRET_KEY = secret_key
client = MongoClient(SECRET_KEY, tlsCAFile=ca)
db = client.dbsparta


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/signin')
def signin():
    return render_template('signin.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


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



@app.route('/view/<num>')
def view(num):
    return render_template('view.html', num=num)

@app.route('/view_content/', methods=['GET'])
def view_content():
    num = request.args.get('num')
    int_num = int(num)
    content_view = [db.musics.find_one({'num': int_num}, {'_id': False})]
    return jsonify({'content_list': content_view})


@app.route('/write')
def write():
    return render_template('write.html')

@app.route("/content", methods=["POST"])
def content():
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


    content_list = list(db.musics.find({}, {'_id': False}))
    count = len(content_list) + 1
    title_receive = request.form["title_give"]
    content_receive = request.form["content_give"]
    star_receive = request.form["star_give"]

    doc = {
        "num" : count,
        "title": title_receive,
        "content": content_receive,
        "star": star_receive,
        'img': img[0],
        's_title': title[0],
        'artist': artist
    }

    db.musics.insert_one(doc)
    return jsonify({"result": "success", "msg": "업로드 완료!"})



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
