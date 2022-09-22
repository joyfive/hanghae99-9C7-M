from flask import Flask, render_template, request, jsonify, request, redirect, url_for, send_from_directory
from bs4 import BeautifulSoup
import requests
import os

from secretkey import secret_key
app = Flask(__name__)

from pymongo import MongoClient
import certifi
import jwt
import datetime
import hashlib

from datetime import datetime, timedelta

ca = certifi.where()

SECRET_KEY = secret_key
client = MongoClient(SECRET_KEY, tlsCAFile=ca)
db = client.dbsparta

@app.route('/favicon.ico')
def favicon():
   return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')

#메인, 리스팅
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/list', methods=['GET'])
def view_list():
    content_list = list(db.musics.find({}, {'_id': False}).sort("num", -1).limit(100))
    return jsonify({'content_list': content_list})

#로그인, 회원가입

@app.route('/home')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"username": payload["id"]})
        return render_template('index.html', user_info=user_info)  #로그인하면 넘어갈 페이지
    except jwt.ExpiredSignatureError:
        return redirect(url_for("index", msg="로그인 시간이 만료되었습니다.")) #로그인 시간 끝나면 나오는 페이지랑 메세지
    except jwt.exceptions.DecodeError:
        return redirect(url_for("index", msg="로그인 정보가 존재하지 않습니다."))

@app.route('/signin')
def signin():
    msg = request.args.get("msg")
    return render_template('signin.html', msg=msg)

@app.route('/sign_in', methods=['POST'])
def sign_in():
    # 로그인
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'username': username_receive, 'password': pw_hash})

    if result is not None:
        payload = {
            'id': username_receive,
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8') #(localhost 하면 주석)(flask하면 주석 지우기)

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()

    doc = {
        "username": username_receive,
        "password": password_hash
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})


@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({"username": username_receive}))
    # print(value_receive, type_receive, exists)
    return jsonify({'result': 'success', 'exists': exists})


# 파라미터값 인풋데이터 크롤링 후 가공된 데이터 반환(write 페이지)
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


#게시판(게시글작성-크롤링 데이터 통합 저장, 게시글 뷰- 매개변수 상세 Url)
@app.route('/view/<num>')
def view(num):
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({'username': payload['id']})
        return render_template('view.html', num=num, user_info=user_info)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("index", msg="로그인 시간이 만료되었습니다."))  # 로그인 시간 끝나면 나오는 페이지랑 메세지
    except jwt.exceptions.DecodeError:
        return redirect(url_for("signin", msg="로그인 정보가 존재하지 않습니다."))

@app.route('/view_content/', methods=['GET'])
def view_content():
    num = request.args.get('num')
    int_num = int(num)
    content_view = [db.musics.find_one({'num': int_num}, {'_id': False})]
    return jsonify({'content_list': content_view})


@app.route('/write')
def write():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({'username': payload['id']})
        return render_template('write.html', user_info=user_info)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("index", msg="로그인 시간이 만료되었습니다."))  # 로그인 시간 끝나면 나오는 페이지랑 메세지
    except jwt.exceptions.DecodeError:
        return redirect(url_for("signin", msg="로그인 정보가 존재하지 않습니다."))

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