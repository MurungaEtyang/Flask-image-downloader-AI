from flask import Flask, render_template, request
from script import ImageDownloadder as pi
import os

app = Flask(__name__)
main_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images/")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/app.py', methods=['POST'])
def download():
    name = request.form['name']
    limit = int(request.form['limit'])
    P = pi()
    P.download(name, limit=limit, directory=main_directory)
    return 'Images downloaded successfully!'

if __name__ == '__main__':
    app.debug = True
    app.run()