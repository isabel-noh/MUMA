from flask import Flask, render_template, request, jsonify
import hashlib
from pymongo import MongoClient
import config # config는 로컬 환경에서는 사용되지 않으므로 지워주셔도 괜찮습니다.
import renderTag # 서브사이드 렌더링에 사용됩니다.
import jwt
import datetime
import requests
from datetime import datetime, timedelta

####### 주의!!! #######
#사용한 라이브러리는 flask, pymongo, dnspython, requests 입니다. 설치하시고 실행해 주세요.
#확인결과, 서버에서는 jwt 암호화를 해준 함수들을 UTF-8로 복호화 시켜줘야 작동하는데, 로컬에서는 이상하게도 복호화 시켜주지 않아야 잘 작동합니다.
#따라서, 제가 서버에 올리는 app.py와 로컬에서 돌리는 app.py가 조금 다르다는 것을 참조해 주셨으면 합니다.
######################

app = Flask(__name__)
client = MongoClient(config.mongoDB) # 각자의 몽고DB와 연동해 주세요.
db = client.dbsparta
SECRET_KEY = config.secret_key # config 처리 해줘야 합니다. 깃허브에서는 숨겨둡니다.
KEY_SECRET = config.key_secret # 저는 리프레시 토큰과 액세스 토큰의 암호화 코드를 각각 달리 지정해 줬습니다. 사용하시려면 두 암호에 아무 문자열이나 입력해주세요.

@app.route('/')
def main():
    acc_token_receive = request.cookies.get('acc_token')
    # try~ catch나 try~ except 같은 예외처리문은 실제로도 쓰인다고 하니 참고로 알아두면 좋겠습니다. if ~ else 와 비슷하지만, 에러코드가 나도 작동하도록 설계된 문법입니다.
    try:
        payload = jwt.decode(acc_token_receive, SECRET_KEY, algorithms=['HS256']) # 이 코드에서 acc 토큰의 디코딩을 시도합니다. 디코딩할 문자열이 없다면 예외처리됩니다. 가능하다면 로그인이 된 페이지를 렌더링할 것입니다.
        return render_template('index.html', head = renderTag.cur_st_login)

    except jwt.ExpiredSignatureError: # 인증키의 시간이 만료되었음을 의미합니다. ref_token이 있다면, 다시 발급하는 절차를 거칩니다.
        try:
            ref_token_receive = request.cookies.get('ref_token')
            payload = jwt.decode(ref_token_receive, KEY_SECRET, algorithms=['HS256'])
            payload['exp'] = datetime.utcnow() + timedelta(seconds=60 * 15)
            acc_token = jwt.encode(payload, SECRET_KEY, algorithm='HS256') # ACCESS TOKEN 생성
            return render_template('index.html', head=renderTag.cur_st_login, acc_token=acc_token)
        except: # ref_token이 발급되지 않은 상태라면 로그인 되지 않은 화면으로 렌더링합니다.
            return render_template('index.html', head=renderTag.cur_st_logout)

    except jwt.exceptions.DecodeError: # 디코딩을 시도할수 없다는 뜻입니다. 어떤 이유로 acc_token 자체가 파괴되었거나, 회원 정보가 일치하지 않는다는 뜻입니다.
        try: # 마찬가지로 똑같은 절차를 밟습니다.
            ref_token_receive = request.cookies.get('ref_token')
            payload = jwt.decode(ref_token_receive, KEY_SECRET, algorithms=['HS256'])
            payload['exp'] = datetime.utcnow() + timedelta(seconds=60 * 15)
            acc_token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')  # ACCESS TOKEN 생성
            return render_template('index.html', head=renderTag.cur_st_login, acc_token=acc_token)
        except:  # ref_token이 발급되지 않은 상태라면 로그인 되지 않은 화면으로 렌더링합니다.
            return render_template('index.html', head=renderTag.cur_st_logout)

@app.route('/login')
def login():
    acc_token_receive = request.cookies.get('acc_token')

    try: # 토큰이 디코딩 가능한 상태는 아직 토큰이 유효함을 의미하므로, 로그인 페이지로 이동해서는 안됩니다. flash 라이브러리를 이용하면 접근제한 메시지를 프론트로 전송할 수 있지만 생략하겠습니다.
        payload = jwt.decode(acc_token_receive, SECRET_KEY, algorithms=['HS256'])
        return render_template('index.html', head=renderTag.cur_st_login)

    except jwt.ExpiredSignatureError:  # 인증키의 시간이 만료되었음을 의미합니다. ref_token이 있다면, 다시 발급하는 절차를 거칩니다.
        try:
            ref_token_receive = request.cookies.get('ref_token')
            payload = jwt.decode(ref_token_receive, KEY_SECRET, algorithms=['HS256'])
            payload['exp'] = datetime.utcnow() + timedelta(seconds=60 * 15)
            acc_token = jwt.encode(payload, SECRET_KEY, algorithm='HS256') # ACCESS TOKEN 생성
            return render_template('index.html', head=renderTag.cur_st_login, acc_token=acc_token)
        except:  # ref_token이 발급되지 않은 상태라면 로그인 페이지로 렌더링합니다.
            return render_template('login.html')

    except jwt.exceptions.DecodeError:  # 디코딩을 시도할수 없다는 뜻입니다. 어떤 이유로 acc_token 자체가 파괴되었거나, 회원 정보가 일치하지 않는다는 뜻입니다.
        try:  # 마찬가지로 똑같은 절차를 밟습니다.
            ref_token_receive = request.cookies.get('ref_token')
            payload = jwt.decode(ref_token_receive, KEY_SECRET, algorithms=['HS256'])
            payload['exp'] = datetime.utcnow() + timedelta(seconds=60 * 15)
            acc_token = jwt.encode(payload, SECRET_KEY, algorithm='HS256') # ACCESS TOKEN 생성
            return render_template('index.html', head=renderTag.cur_st_login, acc_token=acc_token)
        except:  # ref_token이 발급되지 않은 상태라면 로그인 페이지로 렌더링합니다.
            return render_template('login.html')

@app.route('/join')
def join():
    acc_token_receive = request.cookies.get('acc_token')

    try:  # 토큰이 디코딩 가능한 상태는 아직 토큰이 유효함을 의미하므로, 회원가입 페이지로 이동해서는 안됩니다. flash 라이브러리를 이용하면 접근제한 메시지를 프론트로 전송할 수 있지만 생략하겠습니다.
        payload = jwt.decode(acc_token_receive, SECRET_KEY, algorithms=['HS256'])
        return render_template('index.html', head=renderTag.cur_st_login)

    except jwt.ExpiredSignatureError:  # 인증키의 시간이 만료되었음을 의미합니다. ref_token이 있다면, 다시 발급하는 절차를 거칩니다.
        try:
            ref_token_receive = request.cookies.get('ref_token')
            payload = jwt.decode(ref_token_receive, KEY_SECRET, algorithms=['HS256'])
            payload['exp'] = datetime.utcnow() + timedelta(seconds=60 * 15)
            acc_token = jwt.encode(payload, SECRET_KEY, algorithm='HS256') # ACCESS TOKEN 생성
            return render_template('index.html', head=renderTag.cur_st_login, acc_token=acc_token)
        except:
            return render_template('join.html')


    except jwt.exceptions.DecodeError:  # 디코딩을 시도할수 없다는 뜻입니다. 어떤 이유로 acc_token 자체가 파괴되었거나, 회원 정보가 일치하지 않는다는 뜻입니다.
        try:  # 마찬가지로 똑같은 절차를 밟습니다.
            ref_token_receive = request.cookies.get('ref_token')
            payload = jwt.decode(ref_token_receive, KEY_SECRET, algorithms=['HS256'])
            payload['exp'] = datetime.utcnow() + timedelta(seconds=60 * 15)
            acc_token = jwt.encode(payload, SECRET_KEY, algorithm='HS256') # ACCESS TOKEN 생성
            return render_template('index.html', head=renderTag.cur_st_login, acc_token=acc_token)
        except:  # ref_token이 발급되지 않은 상태라면 회원가입 페이지로 렌더링합니다.
            return render_template('join.html')

@app.route("/muse_select", methods=["GET"])
def muse_select():
    doc = []  # 검색을 마친 자료가 들어갈 배열입니다.
    builder_receive = request.args.get("builder_give")
    type_receive = request.args.get("type_give")
    area_receive = request.args.get("area_give")

    museums = list(db.muse_info.find({}, {'_id': False}))  # 박물관의 전체 목록을 museums 변수로 받아옵니다.
    if builder_receive == '국공립':
        for museum in museums:
            if museum["type"] == '국립' or museum["type"] == '공립':
                if type_receive == '박물관전체':
                    if area_receive == '지역전체':
                        doc.append(museum)
                    elif area_receive in museum['addr']:
                        doc.append(museum)
                elif type_receive in museum['name']:
                    if area_receive == '지역전체':
                        doc.append(museum)
                    elif area_receive in museum['addr']:
                        doc.append(museum)
    elif builder_receive == '타입전체':
        for museum in museums:
            if type_receive == '박물관전체':
                if area_receive == '지역전체':
                    doc.append(museum)
                elif area_receive in museum['addr']:
                    doc.append(museum)
            elif type_receive in museum['name']:
                if area_receive == '지역전체':
                    doc.append(museum)
                elif area_receive in museum['addr']:
                    doc.append(museum)

    else:
        for museum in museums:
            if builder_receive in museum["type"]:
                if type_receive == '박물관전체': #str.contains('박물관')
                    if area_receive == '지역전체':
                        doc.append(museum)
                    elif area_receive in museum['addr']:
                        doc.append(museum)
                elif type_receive in museum['name']:
                    if area_receive == '지역전체':
                        doc.append(museum)
                    elif area_receive in museum['addr']:
                        doc.append(museum)

    return jsonify({'filter_list': doc, 'msg': '검색완료!'})

    # 검색 기능
@app.route("/muse_search", methods=["GET"])
def muse_search():
    doc = []
    text_receive = request.args.get("text_give")
    museums = list(db.muse_info.find({}, {'_id': False}))
    for museum in museums:
        if text_receive in museum['name']:
            doc.append(museum)
    return jsonify({'search_list' : doc, 'msg': '검색 완료!'})

# detailpg.html로 연결하면서 해당박물관 데이터를 전송
@app.route('/detail/mm_no/<index>')
def detail(index):
    mm_no = index
    index = int(index)
    museum = db.muse_info.find_one({'index': index})
    img = db.mimgs.find_one({'mm_no': mm_no})
    # 지도 주소 위도, 경도로 변환 : x, y 값
    headers = {
        "X-NCP-APIGW-API-KEY-ID": "afrl6tl1y2",
        "X-NCP-APIGW-API-KEY": "CwhCBEw4LafFurJ2juls3RMtmVy8yYmkXS4fMNTV"
    }
    r = requests.get(f"https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query={museum['addr']}", headers=headers)
    response = r.json()
    # 지도 주소 정보를 찾을 수 없을때 예외 처리
    if response["status"] == "OK":
        if len(response["addresses"]) > 0:
            x = float(response["addresses"][0]["x"])
            y = float(response["addresses"][0]["y"])
        else:
            print("좌표를 찾지 못했습니다")

    return render_template('detail.html', museum = museum, img=img, addr_x = x, addr_y = y)

@app.route('/saveimg', methods=['POST'])
def saveimg():
    mmnum_receive = request.form["mmnum_give"]
    file = request.files["file_give"]

    extension = file.filename.split('.')[-1]

    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')

    filename = f'file-{mytime}'
    save_to = f'static/{filename}.{extension}'
    file.save(save_to)

    doc = {
        'mm_no': mmnum_receive,
        'file': f'{filename}.{extension}'
    }

    db.mimgs.insert_one(doc)

    return jsonify({'msg': '저장 완료!'})


@app.route('/posting', methods=['POST'])
def posting():
    mmnum_receive = request.form["mmnum_give"]
    name_receive = request.form["name_give"]
    score_receive = request.form["score_give"]
    comment_receive = request.form["comment_give"]
    date_receive = request.form["date_give"]
    doc = {
        "m_num": mmnum_receive,
        "username": name_receive,
        "score": score_receive,
        "comment": comment_receive,
        "date": date_receive
    }
    db.posts.insert_one(doc)
    return jsonify({"result": "success", 'msg': '포스팅 성공'})

@app.route("/get_posts", methods=['GET'])
def get_posts():
    m_num = request.args.get('num_give')
    posts = list(db.posts.find({'m_num': m_num}).sort("date", -1))
    for post in posts:
        post["_id"] = str(post["_id"])
    return jsonify({"result": "success", "msg": "포스팅을 가져왔습니다.", "posts": posts})

@app.route('/delete', methods=['POST'])
def delete():
    # 삭제하기
    m_num = request.args.get('num_give')
    post_id_receive = request.form["post_id_give"]
    posts = list(db.posts.find({'m_num': m_num}).sort("date", -1))
    for post in posts:
        if str(post["_id"]) == post_id_receive:
            db.posts.delete_one({"_id":post["_id"]})
    return jsonify({'result': 'success', 'msg': 'deleted'})

# @app.route('/delete_post', methods=['DELETE'])
# def delete_post():

@app.route("/muse_info", methods=["GET"])
def muse_get():
    all_muse = list(db.muse_info.find({},{'_id':False}))
    return jsonify({'mnt': all_muse})

@app.route("/muse_show", methods=["GET"])
def show_muse():
    num_receive = request.args.get('num_give')
    muse_data = db.muse_info.find_one({'index':int(num_receive)},{'_id':False})
    return jsonify({'muse_data': muse_data})

@app.route('/api/join', methods=['POST']) # 회원가입 기능입니다. 시간이 남는다면 서버에서 2차 유효성검사를 실시해 보겠습니다.
def api_join():
    id_receive = request.form['id_give']
    email_receive = request.form['email_give']
    pw_receive = request.form['pw_give']
    nickname_receive = request.form['nickname_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
    db.register.insert_one({ 'email': id_receive + email_receive, 'pw': pw_hash, 'nick': nickname_receive})

    return jsonify({'result': 'success', 'msg': '회원가입 완료!'})

@app.route('/api/join/check_email', methods=['POST'])
def api_checkEmail():
    id_receive = request.form['id_give']
    email_receive = request.form['email_give']
    email_addr = id_receive + email_receive

    regi = db.register.find_one({'email': email_addr})

    if regi == None:
        return jsonify({'result': 'success', 'msg': '사용 가능한 이메일입니다.'})
    else:
        return jsonify({'result': 'failure', 'msg': '사용중인 이메일입니다.'})

@app.route('/api/join/check_nick', methods=['POST'])
def api_checkNick():
    nick_receive = request.form['nickname_give']

    regi = db.register.find_one({'nick': nick_receive})

    if regi is None:
        return jsonify({'result': 'success', 'msg': '사용 가능한 닉네임입니다.'})
    else:
        return jsonify({'result': 'failure', 'msg': '사용중인 닉네임입니다.'})

@app.route('/api/login', methods=['POST'])
def api_login():
    # 로그인
    email_receive = request.form['email_give']
    pw_receive = request.form['pw_give']
    keep_receive = request.form['chk_keep']
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
    result = db.register.find_one({'email': email_receive, 'pw': pw_hash})

    if result is not None:
        if keep_receive == 'true':
            payload = {
             'id': email_receive,
             'exp': datetime.utcnow() + timedelta(seconds=60 * 15) # 로그인 15분 유지
            }
            acc_token = jwt.encode(payload, SECRET_KEY, algorithm='HS256') # ACCESS TOKEN 생성
            payload = {
                'id': email_receive,
                'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24 * 7)  # 로그인 7일 유지
            }
            ref_token = jwt.encode(payload, KEY_SECRET, algorithm='HS256') # REFRESH TOKEN 생성
            return jsonify({'result': 'success', 'acc_token': acc_token, 'ref_token': ref_token})
        else:
            payload = {
                'id': email_receive,
                'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 4)  # 로그인 4시간 유지
            }
            acc_token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
            return jsonify({'result': 'success', 'acc_token': acc_token})

    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디와 비밀번호를 확인해주세요.'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)