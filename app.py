from flask import Flask, render_template, request, jsonify
app = Flask(__name__)
import certifi
from pymongo import MongoClient

client = MongoClient('mongodb+srv://id:password@cluster0.0vjef.mongodb.net/Cluster0?retryWrites=true&w=majority',tlsCAFile=certifi.where())
db = client.dbsparta

#HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')

    #   필터 기능
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
def muse_filter():
    doc = []
    text_receive = request.args.get("text_give")
    museums = list(db.muse_info.find({}, {'_id': False}))
    for museum in museums:
        if text_receive in museum['name']:
            doc.append(museum)
    return jsonify({'search_list' : doc, 'msg': '검색 완료!'})
    # detailpg.html로 연결하면서 index 데이터를 전송
    return jsonify({'search_list': doc, 'msg': '검색완료!'})

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

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
