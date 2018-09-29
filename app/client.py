import requests
import json
from PIL import ImageGrab, Image
import clipboard

def upload():
    # 从剪切板获取图片上传
    url = 'http://127.0.0.1:18800/'

    headers = {'Content-Type': 'application/json'}

    payload = {'username':'demo', 'password':'demo'}

    r = requests.post(url,headers=headers, data=json.dumps(payload))

    token = r.text 

    upload_url = 'http://127.0.0.1:18800/upload'

    files = {'image001': open(r'd:/tmp0001.jpg', 'rb')}

    h1 = {'token':token}

    ru = requests.post(upload_url, headers=h1, files=files)

    clipboard.copy(ru.text)

if __name__ == '__main__':
    im= ImageGrab.grabclipboard()
    if isinstance(im, Image.Image):
        im.save(r'd:/tmp0001.jpg')
        upload()