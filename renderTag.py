# 서브사이드 렌더링 구현을 위한 코드입니다. 해당 코드는 메인페이지의 헤드에 들어가 로그인과 로그아웃시 각각 다른 결과를 출력합니다.

tag_a = "<span class='headerBtn'>"
tag_b = "<button onclick='open_search()'><img src='https://img.icons8.com/ios-glyphs/30/000000/search--v1.png'/></button>"
tag_c = "<a href='/login'><button type='button' class='btn btn-light'>Login</button></a>"
tag_d = "<a href='/join'><button type='button' class='btn btn-outline-dark'>Sign-Up</button></a>"
tag_e = "</span>"

tag_f = "<a href='/mypage'><button type='button' class='btn btn-light'>Mypage</button></a>"
tag_g = "<button style='border: 0px' onclick='logout()' type='button' class='btn btn-outline-dark'>Logout</button></a>"

cur_st_logout = tag_a + "\n" + tag_b + "\n" + tag_c + "\n" + tag_d + "\n" + tag_e
cur_st_login = tag_a + "\n" + tag_b + "\n" + tag_f + "\n" + tag_g + "\n" + tag_e

a_detail_pg = "<div class='mystar'>"
b_detail_pg = "<select class='form-select' id='inputGroupSelect01' aria-label='Default select example'><option selected>별점주기</option><option value='5'>⭐⭐⭐⭐⭐</option><option value='4'>⭐⭐⭐⭐</option><option value='3'>⭐⭐⭐</option><option value='2'>⭐⭐</option><option value='1'>⭐</option></select></div><div class='input-group mb-3'><input type='text' class='form-control' id='textarea-post' placeholder='의견을 자유롭게 적어주세요.' aria-label='Recipient's username' aria-describedby='button-addon3'><button class='btn btn-outline-secondary' type='button' id='button-addon3' onclick='post()'>입력</button></div>"
c_detail_pg = "</div>"
d_detail_pg = "<div><p>죄송해요! 글쓰기와 대표 이미지 업로드는 회원만 할 수 있어요!</p></div>"

current_login = a_detail_pg + '\n' + b_detail_pg + '\n' + c_detail_pg
current_logout = a_detail_pg + '\n' + d_detail_pg + '\n' + c_detail_pg

img_login = "<input type='file' class='form-control' id='inputGroupFile04' aria-describedby='inputGroupFileAddon04' aria-label='Upload'><button class='btn btn-outline-secondary' type='button' id='inputGroupFileAddon04' onclick='save_img()'>사진 등록</button>"
img_logout = ""