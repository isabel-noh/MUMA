from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

import hashlib

from pymongo import MongoClient
import config
client = MongoClient(config.mongoDB)
db = client.dbsparta

@app.route('/join') # html join으로 통일 변경
def join():
    return render_template('join.html')

@app.route('/api/join', methods=['POST'])
def api_join():
    id_receive = request.form['id_give']
    email_receive = request.form['email_give']
    pw_receive = request.form['pw_give']
    nickname_receive = request.form['nickname_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
    db.regi_test.insert_one({'id': id_receive, 'pw': pw_hash, 'nick': nickname_receive, 'email': id_receive + email_receive})
    return jsonify({'result': 'success', 'msg': '회원가입 완료!'})

@app.route('/api/join/check_email', methods=['POST'])
def api_checkEmail():
    id_receive = request.form['id_give']
    email_receive = request.form['email_give']
    email_addr = id_receive + email_receive

    regi = db.regi_test.find_one({'email': email_addr})

    if regi is None:
        return jsonify({'result': 'success', 'msg': '사용 가능한 이메일입니다.'})
    else:
        return jsonify({'result': 'failure', 'msg': '사용중인 이메일입니다.'})

@app.route('/api/join/check_nick', methods=['POST'])
def api_checkNick():
    nick_receive = request.form['nickname_give']

    regi = db.regi_test.find_one({'nick': nick_receive})

    if regi is None:
        return jsonify({'result': 'success', 'msg': '사용 가능한 닉네임입니다.'})
    else:
        return jsonify({'result': 'failure', 'msg': '사용중인 닉네임입니다.'})
