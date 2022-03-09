from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
import requests

app = Flask(__name__)

client = MongoClient('mongodb://test:sparta@cluster0-shard-00-00.ite7q.mongodb.net:27017,cluster0-shard-00-01.ite7q.mongodb.net:27017,cluster0-shard-00-02.ite7q.mongodb.net:27017/Cluster0?ssl=true&replicaSet=atlas-1371nk-shard-0&authSource=admin&retryWrites=true&w=majority')
db = client.dbsparta


@app.route('/')
def main():
    # DB에서 저장된 단어 찾아서 HTML에 나타내기
    return render_template("index.html")


#detailpg.html로 연결하면서 mnt_no 데이터를 전송
@app.route('/detail/mm_no/<index>')
def detail(index):
    index = int(index)
    museum = db.muse_info.find_one({'index': index})
    return render_template('detail.html', museum = museum)



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)