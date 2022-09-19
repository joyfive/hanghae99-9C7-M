from flask import Flask, render_template
app = Flask(__name__)

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

@app.route('/write')
def write():
   return render_template('write.html')


if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)