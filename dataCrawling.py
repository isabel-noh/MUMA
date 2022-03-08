import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient

import config

client = MongoClient(config.mongoDB)
db = client.dbsparta

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('http://api.data.go.kr/openapi/tn_pubr_public_museum_artgr_info_api?serviceKey=' + config.decodingKey + '&pageNo=1&numOfRows=1522&type=xml', headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

items = soup.select('item')

for item in items:
    all_muse = list(db.muse_info.find({}, {'_id': False}))
    muse_no = (len(all_muse) + 1)

    muse_name = item.find('fcltynm').text
    muse_type = item.find('fcltytype').text
    muse_addr = item.find('rdnmadr').text
    muse_lat = item.find('latitude').text
    muse_long = item.find('longitude').text
    muse_url = item.find('homepageurl').text
    muse_open = item.find('weekdayoperopenhhmm').text
    muse_close = item.find('weekdayopercolsehhmm').text
    holi_open = item.find('holidayoperopenhhmm').text
    holi_close = item.find('holidaycloseopenhhmm').text
    muse_rest = item.find('rstdeinfo').text
    muse_phone = item.find('phonenumber').text
    adult_charge = item.find('adultchrge').text
    young_charge = item.find('yngbgschrge').text
    child_charge = item.find('childchrge').text
    etc_charge = item.find('etcchrgeinfo').text
    muse_intr = item.find('fcltyintrcn').text
    referencedate = item.find('referencedate').text

    # 자료들은 모두 몽고DB에 저장해 두었습니다. 딕셔너리를 보시고 적절한 정보를 꺼내 쓰시면 잘 작동할 것입니다.

    doc = {'index':muse_no, # index : 박물관 번호
           'name': muse_name, # name : 박물관 이름
           'type': muse_type, # type : 공/사립 구분
           'addr': muse_addr, # addr : 도로명주소
           'url': muse_url, # url : 홈페이지 주소
           'lat':muse_lat, # lat : 위도
           'long':muse_long, # long : 경도
           'open':muse_open, # open : 평일 오픈시간
           'close':muse_close, # close : 평일 마감시간
           'holi_open': holi_open,  # holi_open : 휴일 오픈시간
           'holi_close': holi_close,  # holi_close : 휴일 마감시간
           'rest_info':muse_rest, # rest_info : 휴무정보
           'phone':muse_phone, # phone : 관리주체 전화번호
           'introduce':muse_intr, # introduce : 간략소개(없는 경우가 아주 많습니다.)
           'adult_charge':adult_charge, # adult_charge : 어른 관람료
           'young_charge':young_charge, # young_charge : 청소년 관람료
           'child_charge':child_charge, # child_charge : 어린이 관람료
           'etc_charge':etc_charge, # etc_charge : 관람료 기타정보
           'date':referencedate} # date : 데이터 기준일자

    db.muse_info.insert_one(doc)
