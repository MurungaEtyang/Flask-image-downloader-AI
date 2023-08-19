from flask import Flask, render_template, request
from script import ImageDownloadder as pi
import progressbar
import os

app = Flask(__name__)
main_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images/")

@app.route('/')
def home():
    return render_template('public/index.html')

@app.route('/app.py', methods=['POST'])
def download():
    name = request.form['name']
    limit = int(request.form['limit'])
    p = progressbar.ProgressBar(maxval=limit)
    P = pi()
    P.download(name, limit=limit)

    return render_template("output.html")


if __name__ == '__main__':
    app.debug = True
    app.run()