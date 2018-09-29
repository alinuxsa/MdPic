import requests
import json
from PIL import ImageGrab, Image
import clipboard, pickle
import time, os

class Client():
    """获取token"""
    def __init__(self):
        self.url = 'http://127.0.0.1:18800/'
        self.headers = {'Content-Type': 'application/json'}
        self.payload = {'username':'demo', 'password':'demo'}
        self.pkiFile = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'token.pki')

    def getToken(self):
        # 获取token
        token = {}
        r = requests.post(self.url,headers=self.headers, data=json.dumps(self.payload))
        t = r.text 
        timestamp = int(time.time())
        token.setdefault('token', t)
        token.setdefault('timestamp', timestamp)
        with open(self.pkiFile, 'wb') as f:
            pickle.dump(token,f)

    def showToken(self):
        # 从文件获取token
        with open(self.pkiFile, 'rb') as f:
            t = pickle.load(f)
            return t.get('token')

    def tokenExpired(self):
        # 验证是否过期
        if not os.path.exists(self.pkiFile):
            self.getToken()
        with open(self.pkiFile, 'rb') as f:
            token = pickle.load(f)
        if int(time.time()) - token.get('timestamp') > 600:
            return True
        else:
            return False


    def upload(self):
        # 从剪切板获取图片上传

        upload_url = self.url + 'upload'
        files = {'image001': open(r'd:/tmp0001.jpg', 'rb')}
        h1 = {'token':token}
        ru = requests.post(upload_url, headers=h1, files=files)
        clipboard.copy(ru.text)

if __name__ == '__main__':
    im= ImageGrab.grabclipboard()
    if isinstance(im, Image.Image):
        print("剪切板有图片")
        c = Client()
        if c.tokenExpired():
            print('token过期,重新获取')
            c.getToken()
        token = c.showToken()
        im.save(r'd:/tmp0001.jpg')
        c.upload()