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