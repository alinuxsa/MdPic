import requests
import json
from PIL import ImageGrab, Image

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

    print(ru.text)

if __name__ == '__main__':
    print('1')
    im= ImageGrab.grabclipboard()
    if isinstance(im, Image.Image):
        print('上传')
        # with open(r'd:\pic.log', 'a+') as f:
        #     from datetime import datetime
        #     now = datetime.now()
        #     f.write(str(now))
        im.save(r'd:/tmp0001.jpg')
        upload()