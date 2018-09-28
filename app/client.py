import requests
import json

url = 'http://127.0.0.1:18800/'

headers = {'Content-Type': 'application/json'}

payload = {'username':'demo', 'password':'demo'}

r = requests.post(url,headers=headers, data=json.dumps(payload))

token = r.text 

upload_url = 'http://127.0.0.1:18800/upload'

files = {'image001': open(r'd:/1.png', 'rb')}

h1 = {'token':token}

ru = requests.post(upload_url, headers=h1, files=files)

print(ru.text)