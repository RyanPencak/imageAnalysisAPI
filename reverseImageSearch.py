import requests
from googlesearch import search

filePath = './static/img/testImg.jpg'
searchUrl = 'http://www.google.hr/searchbyimage/upload'
multipart = {'encoded_image': (filePath, open(filePath, 'rb')), 'image_content': ''}
response = requests.post(searchUrl, files=multipart, allow_redirects=False)
fetchUrl = response.headers['Location']
print(fetchUrl)

for j in search(fetchUrl, tld="co.in", num=3, stop=1, pause=2):
    print(j)
