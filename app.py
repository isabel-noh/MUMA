from flask import Flask, render_template, request, jsonify
app = Flask(__name__)
import certifi
from pymongo import MongoClient

client = MongoClient('mongodb+srv://id:passwor@cluster0.0vjef.mongodb.net/Cluster0?retryWrites=true&w=majority',tlsCAFile=certifi.where())
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

    #   필터 기능을 3중으로...하는 중입니다.
@app.route("/muse_select", methods=["GET"])
def mnt_select():
    doc = []  # 검색을 마친 자료가 들어갈 배열입니다.
    area_receive = request.args.get("area_give")
    museums = list(db.muse_info.find({}, {'_id': False}))  # 산의 전체 목록을 mountains 변수로 받아옵니다.
    for museum in museums:
        if area_receive in museums['addr']:  # 산의 세부 설명에서 mnt_receive로 받은 검색어를 찾아봅니다.
            doc.append(museum)  # 일치하는 명산의 번호를 doc 배열에 집어넣습니다.
    return jsonify({'search_list': doc, 'msg': '검색완료!'})

# index_sub로 연결하면서 mnt_no 데이터를 전송
@app.route('/detail_pg', methods=['GET'])
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
    app.run('0.0.0.0', port=5001, debug=True)
