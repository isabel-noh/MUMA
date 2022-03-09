from flask import Flask, render_template, request, jsonify, redirect, url_for
import hashlib
from pymongo import MongoClient
import config
import jwt
import datetime
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename

client = MongoClient(config.mongoDB)
db = client.dbsparta
SECRET_KEY=config.secret_key

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/api/login', methods=['POST'])
def api_login():
    # 로그인
    email_receive = request.form['email_give']
    pw_receive = request.form['pw_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
    result = db.regi_test.find_one({'email': email_receive, 'pw': pw_hash})

    if result is not None:
        payload = {
         'id': email_receive,
         'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})