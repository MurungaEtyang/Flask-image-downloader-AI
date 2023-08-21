from flask import Flask, render_template, request, url_for
from script import ImageDownloadder as pi
import os
app = Flask(__name__)
main_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images/")

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('./home.html')


@app.route('/app.py', methods=['POST', 'GET'])
def download():
    name = request.form['name']
    limit = int(request.form['limit'])
    P = pi()
    P.download(name, limit=limit)
    return render_template('./output.html')


if __name__ == '__main__':
    app.debug = True
    app.run()
