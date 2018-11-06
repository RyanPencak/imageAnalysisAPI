from flask import Flask, render_template, request, jsonify, send_file
from flask_uploads import UploadSet, configure_uploads, IMAGES
from urllib.request import urlopen,build_opener,HTTPCookieProcessor
from http.cookiejar import CookieJar
from PIL import Image, ImageChops
import requests
import re
import os
# import shutil

app = Flask(__name__)

photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
configure_uploads(app, photos)

@app.route('/upload', methods=['POST'])
def upload():
    if 'queryImg' in request.files:
        # shutil.rmtree('static/img')
        img_path = './static/img/testImg.jpg'
        if os.path.exists(img_path):
            os.remove(img_path)
        filename = photos.save(request.files['queryImg'], folder=None, name='testImg.jpg')
        return filename
    return render_template('upload.html')

@app.route('/getelaoutput', methods=['GET'])
def getELA():
    if os.path.exists('../static/img/output.jpg'):
        return (send_file('../static/img/output.jpg', mimetype='image/jpg'))
        # return send_file(io.BytesIO(ela_path.read()),
        #              attachment_filename='output.jpg',
        #              mimetype='image/jpg')

    return None

@app.route("/imagesearch", methods=['POST'])
def imageLookup():
    if 'queryImg' in request.files:
        img_path = './static/img/lookupImg.jpg'
        if os.path.exists(img_path):
            os.remove(img_path)

        # shutil.rmtree('static/img')
        filename = photos.save(request.files['queryImg'], folder=None, name='lookupImg.jpg')

        cj = CookieJar()
        opener = build_opener(HTTPCookieProcessor(cj))
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17')]

        filePath = './static/img/lookupImg.jpg'
        searchUrl = 'http://www.google.hr/searchbyimage/upload'
        multipart = {'encoded_image': (filePath, open(filePath, 'rb')), 'image_content': ''}
        response = requests.post(searchUrl, files=multipart, allow_redirects=False)
        fetchUrl = response.headers['Location']

        sourceCode = opener.open(fetchUrl).read().decode('utf-8')

        links = re.findall(r'<div class="rc"><div class="r"><a href="(.*?)"',sourceCode)

        return(jsonify(links))

@app.route("/ela", methods=['POST'])
def ELA():
    if 'queryImg' in request.files:
        ORIG = './static/img/elaImg.jpg'
        TEMP = './static/img/temp.jpg'
        SCALE = 10

        if os.path.exists(ORIG):
            os.remove(ORIG)
        if os.path.exists(TEMP):
            os.remove(TEMP)
        if os.path.exists('./imageAnalysis/img/output.jpg'):
            os.remove('./imageAnalysis/img/output.jpg')

        # shutil.rmtree('static/img')
        filename = photos.save(request.files['queryImg'], folder=None, name='elaImg.jpg')

        original = Image.open(ORIG)
        original.save(TEMP, quality=75)
        temporary = Image.open(TEMP)

        diff = ImageChops.difference(original, temporary)
        d = diff.load()
        WIDTH, HEIGHT = diff.size
        for x in range(WIDTH):
            for y in range(HEIGHT):
                d[x, y] = tuple(k * SCALE for k in d[x, y])

        diff.save('./imageAnalysis/img/output.jpg')
        diff.show()

        im = Image.open('./imageAnalysis/img/output.jpg').convert('L')
        pixels = im.getdata()

        # 0 (pitch black) and 255 (bright white)
        black_thresh = 30
        pixels_length = len(pixels)
        nblack = 0

        for pixel in pixels:
            if pixel < black_thresh:
                nblack += 1

        return (send_file('img/output.jpg', mimetype='image/jpg'))
        # return ("Pixel Change Percentage: {0:.2f}%".format((pixels_length - nblack) / pixels_length * 100))
