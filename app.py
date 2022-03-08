from flask import Flask, render_template, request, jsonify
app = Flask(__name__)
import certifi
from pymongo import MongoClient

import hashlib

client = MongoClient('mongodb+srv://id:password@cluster0.0vjef.mongodb.net/Cluster0?retryWrites=true&w=majority',tlsCAFile=certifi.where())
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

    #   필터 기능을 3중으로...하는 중입니다.
@app.route("/muse_select", methods=["GET"])
def mnt_select():
    doc = []  # 검색을 마친 자료가 들어갈 배열입니다.
    builder_receive = request.args.get("builder_give")
    type_receive = request.args.get("type_give")
    area_receive = request.args.get("area_give")

    museums = list(db.muse_info.find({}, {'_id': False}))  # 박물관의 전체 목록을 museums 변수로 받아옵니다.
    if builder_receive == '국공립':
        for museum in museums:
            if museum["type"] == '국립' or museum["type"] =='공립':
    elif builder_receive == '타입전체':
        for museum in museums:
            doc.append(museum)
    else:
        for museum in museums:
            if builder_receive in museum["type"]:
                doc.append(museum)

    return jsonify({'search_list': doc, 'msg': '검색완료!'})

# detailpg.html로 연결하면서 index 데이터를 전송
@app.route('/detail_pg', methods=["GET"])
def detail_pg():
    index = request.args.get('index')
    return render_template('detailpg.html', index = index)

@app.route("/muse_info", methods=["GET"])
def muse_get():
    all_muse = list(db.muse_info.find({},{'_id':False}))
    return jsonify({'mnt': all_muse})

@app.route("/muse_show", methods=["GET"])
def show_muse():
    num_receive = request.args.get('num_give')
    muse_data = db.muse_info.find_one({'index':int(num_receive)},{'_id':False})
    return jsonify({'muse_data': muse_data})

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

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)