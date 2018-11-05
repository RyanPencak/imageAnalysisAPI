from urllib.request import urlopen,build_opener,HTTPCookieProcessor
from http.cookiejar import CookieJar
# from googlesearch import search
import requests
import re

def imageLookup():
    # googlepath = 'http://google.com/searchbyimage?'

    cj = CookieJar()
    opener = build_opener(HTTPCookieProcessor(cj))
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17')]

    filePath = './static/img/testImg.jpg'
    searchUrl = 'http://www.google.hr/searchbyimage/upload'
    multipart = {'encoded_image': (filePath, open(filePath, 'rb')), 'image_content': ''}
    response = requests.post(searchUrl, files=multipart, allow_redirects=False)
    fetchUrl = response.headers['Location']

    sourceCode = opener.open(fetchUrl).read().decode('utf-8')

    links = re.findall(r'<div class="rc"><div class="r"><a href="(.*?)"',sourceCode)

    return(links)


imageLookup()
