from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

from pymongo import MongoClient
import certifi

ca = certifi.where()

client = MongoClient('mongodb+srv://DaminAn:ekals3939@cluster0.hd1bg.mongodb.net/?retryWrites=true&w=majority',
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


@app.route("/content", methods=["POST"])
def content():
    title_receive = request.form["title_give"]
    comment_receive = request.form["comment_give"]
    star_receive = request.form["star_give"]

    doc = {
        "title": title_receive,
        "comment": comment_receive,
        "star": star_receive
    }

    db.musics.insert_one(doc)
    return jsonify({"result": "success", "msg": "업로드 완료!"})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
