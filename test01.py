import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
import certifi

from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

ca = certifi.where()
client = MongoClient('mongodb+srv://DaminAn:ekals3939@cluster0.hd1bg.mongodb.net/?retryWrites=true&w=majority',
                     tlsCAFile=ca)
db = client.dbsparta
jclient = MongoClient('mongodb+srv://joyfive:whdlvkdlqm999@cluster0.omhyorx.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
jdb = jclient.dbsparta

# https://www.genie.co.kr/detail/songInfo?xgnm=97582507
# https://www.genie.co.kr/detail/albumInfo?axnm=82842800



# print(img,title,artist)

#기쁨, 인풋박스에서 파라미터값 받아서 크롤링 데이터 프론트 전달완료
@app.route('/')
def home():
   return render_template('album.html')

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

#----------------------------------------------------------------------
#도원

@app.route('/signin')
def signin():
    return render_template('signin.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')

#----------------------------------------------------------------------
#다민

#
# @app.route('/view')
# def view():
#     return render_template('view.html')

@app.route('/view/<num>')
def viewer(num):
    # content_view = db.musics.find_one({'num': num}, {'_id': False})
    return render_template('view.html', num=num)


@app.route('/write')
def write():
    return render_template('write.html')

@app.route("/content", methods=["POST"])
def content():
    content_list = list(db.musics.find({}, {'_id': False}))
    count = len(content_list) + 1
    title_receive = request.form["title_give"]
    content_receive = request.form["content_give"]
    star_receive = request.form["star_give"]

    doc = {
        "num" : count,
        "title": title_receive,
        "content": content_receive,
        "star": star_receive
    }

    db.musics.insert_one(doc)
    return jsonify({"result": "success", "msg": "업로드 완료!"})









if __name__ == '__main__':
    app.run('0.0.0.0', port=5050, debug=True)

    # from flask import Flask, render_template, request, jsonify, redirect, url_for
    # from pymongo import MongoClient
    # import requests
    #
    # app = Flask(__name__)
    #
    # client = MongoClient('내AWS아이피', 27017, username="아이디", password="비밀번호")
    # db = client.dbsparta_plus_week2
    #
    #
    # @app.route('/')
    # def main():
    #     # DB에서 저장된 단어 찾아서 HTML에 나타내기
    #     return render_template("index.html")
    #
    #
    # @app.route('/detail/<keyword>')
    # def detail(keyword):
    #     # API에서 단어 뜻 찾아서 결과 보내기
    #     return render_template("detail.html", word=keyword)
    #
    #
    # @app.route('/api/save_word', methods=['POST'])
    # def save_word():
    #     # 단어 저장하기
    #     return jsonify({'result': 'success', 'msg': '단어 저장'})
    #
    #
    # @app.route('/api/delete_word', methods=['POST'])
    # def delete_word():
    #     # 단어 삭제하기
    #     return jsonify({'result': 'success', 'msg': '단어 삭제'})
    #
    #
    # if __name__ == '__main__':
    #     app.run('0.0.0.0', port=5000, debug=True)