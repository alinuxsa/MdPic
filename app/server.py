# coding:utf-8
from flask import Flask, request, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature
import os, time
import hashlib


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///api.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'guess me'
app.config['JSON_AS_ASCII'] = False
app.config['UPLOAD_FOLDER'] = 'static/'
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg', 'gif'])
db = SQLAlchemy(app)

msg_default = {
    "msg": "invalid args"
}

def allow_file(filename):
        return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


def gen_filename(filename):
    file_format = filename.split('.')[-1]
    timestamp = time.time()
    tmp_str = '{}{}'.format(timestamp, filename)
    return (hashlib.md5(tmp_str.encode('utf-8')).hexdigest()) + "." +  file_format



class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(200))

    def gen_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            # token过期
            return None
        except BadSignature:
            # token无效
            return None
        user = User.query.get(data['id'])
        return user

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    def verify_password(self, password):
        # 验证密码
        return check_password_hash(self.password_hash, password)

    @password.setter
    def password(self, password):
        # 生成密码
        self.password_hash = generate_password_hash(password)

# 获取token
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username', None)
        password = data.get('password', None)
        print(username, password)
        if username and password:
            user = User.query.filter_by(username=username).first()
            if user is not None and user.verify_password(password):
                token = user.gen_auth_token()
                return token
            else:
                return jsonify(msg_default)
        else:
            return jsonify(msg_default)
    else: 
        return jsonify(msg_default)

# 上传图片
@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        upload_file = request.files['image001']
        token = request.headers.get('token')
        u1 = User.verify_auth_token(token)
        if u1 is not None and u1 is not False:
            print("token有效")
            if upload_file:
                filename = gen_filename(upload_file.filename)
                print("获取到filename {}".format(filename))
                upload_file.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename))
                ext_link = url_for('static', filename=filename,  _external=True, _scheme='https')
                return ext_link
        else:
            msg = {"msg":"invalid token"}
            return jsonify(msg)
    else:
        return jsonify(msg_default)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=18800, debug=False)

