from flask import Flask, render_template, request
from flask_uploads import UploadSet, configure_uploads, IMAGES
import shutil
import os

app = Flask(__name__)

photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
configure_uploads(app, photos)

@app.route('/')
def hello():
    return "hello\n"

@app.route('/upload', methods=['POST'])
def upload():
    if 'queryImg' in request.files:
        shutil.rmtree('static/img')
        filename = photos.save(request.files['queryImg'])
        return filename
    return render_template('upload.html')


@app.route("/analyze")
def hello_world():
  return "Analyzed!\n"
