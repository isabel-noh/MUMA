from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
import config
client = MongoClient(config.mongoDB)
db = client.dbsparta

import hashlib
# 기본적으로 요청받은 비밀번호들은 해쉬랩에 의해서 암호화되어 저장됩니다. 따라서, 로그인 정보와 활용하기 위해서는 복호화 과정도 필요합니다.

# 아래는 유효성을 검사하는 메소드입니다.
def checkValid(id, email, pw, pw_c, nick):
    if not id.strip():
        return {'msg':'전송실패'}
    if email == '0':
        return {'msg': '이메일을 선택해 주세요!'}
    if not nick.strip():
        return {'msg': '닉네임을 입력해 주세요!'}
    if not nick.isalnum():
        return {'msg': '닉네임에는 특수문자를 입력할 수 없습니다!'}
    if int(len(nick)) > 8:
        return {'msg': '닉네임은 8자 이내로 입력해 주세요!'}
    if not pw.strip():
        return {'msg': '비밀번호를 입력해 주세요!'}
    if pw != pw_c:
        return {'msg': '비밀번호 일치를 확인해 주세요!'}
    if pw.isalnum():
        return {'msg': '비밀번호에 특수문자를 넣어주세요!'}
    if int(len(pw)) > 12 or 8 > int(len(pw)):
        return {'msg': '비밀번호는 8~12자로 입력해 주세요!'}
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
    db.regi_test.insert_one({'id': id, 'pw': pw_hash, 'nick': nick})
    return {'msg': '회원가입 완료!'}

@app.route('/join')
def join():
    return render_template('join.html')

@app.route('/api/join', methods=['POST'])
def api_join():
    id_receive = request.form['id_give']
    email_receive = request.form['email_give']
    pw_receive = request.form['pw_give']
    pw_con_receive = request.form['pw_conf_give']
    nickname_receive = request.form['nickname_give']

    result = checkValid(id_receive, email_receive, pw_receive, pw_con_receive, nickname_receive) # 유효성 검사 시작
    return jsonify(result) # 결과메시지 전송
