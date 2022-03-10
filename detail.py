from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
from datetime import datetime
import requests
import certifi
import hashlib

app = Flask(__name__)

client = MongoClient(config.mongoDB)
db = client.dbsparta

@app.route('/')
def main():
    # DB에서 저장된 단어 찾아서 HTML에 나타내기
    return render_template("index.html")

    #   필터 기능
@app.route("/muse_select", methods=["GET"])
def mnt_select():
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
                if type_receive == '박물관전체':  # str.contains('박물관')
                    if area_receive == '지역전체':
                        doc.append(museum)
                    elif area_receive in museum['addr']:
                        doc.append(museum)
                elif type_receive in museum['name']:
                    if area_receive == '지역전체':
                        doc.append(museum)
                    elif area_receive in museum['addr']:
                        doc.append(museum)

    return jsonify({'search_list': doc, 'msg': '검색완료!'})


# detailpg.html로 연결하면서 해당박물관 데이터를 전송
@app.route('/detail/mm_no/<index>')
def detail(index):
    index = int(index)
    museum = db.muse_info.find_one({'index': index})
    imgs = list(db.muse_imgs.find({'mm_no': index}))
    img = []
    for img in imgs:    # 가장 나중에 넣은 사진을 가져오게 하기
        img = img
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

@app.route('/save_img', methods=['POST'])
def save_img():
    mmnum_receive = request.form["mmnum_give"]
    file = request.files["file_give"]
    mm_no = int(mmnum_receive)      # 나중에 동일한 방식으로 index 이용하기 위해 숫자변환

    extension = file.filename.split('.')[-1]

    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')

    filename = f'file-{mytime}'
    save_to = f'static/{filename}.{extension}'
    file.save(save_to)

    doc = {
        'mm_no': mm_no,
        'file': f'{filename}.{extension}'
    }

    db.muse_imgs.insert_one(doc)

    return jsonify({'msg': '사진 등록 완료!'})


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
    all_muse = list(db.muse_info.find({}, {'_id': False}))
    return jsonify({'mnt': all_muse})

@app.route("/muse_show", methods=["GET"])
def show_muse():
    num_receive = request.args.get('num_give')
    muse_data = db.muse_info.find_one({'index': int(num_receive)}, {'_id': False})
    return jsonify({'muse_data': muse_data})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)