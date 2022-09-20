from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

from pymongo import MongoClient
import certifi

ca = certifi.where()

client = MongoClient('mongodb+srv://DaminAn:ekals3939@cluster0.hd1bg.mongodb.net/Cluster0?retryWrites=true&w=majority',
                     tlsCAFile=ca)
db = client.dbsparta


@app.route('/')
def main():
    return render_template('main.html')


@app.route('/signin')
def signin():
    return render_template('signin.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/view')
def view():
    return render_template('view.html')

@app.route('/viewer', methods=["GET"])
def viewer():
    # content_view = db.musics.find_one()
    return render_template('view.html')

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
    app.run('0.0.0.0', port=5000, debug=True)
