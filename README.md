# 환경 세팅

1. Visual Studio Code 터미널 켜기
<br/>

2. 가상환경 설치
- python -m venv venv
<br/>

3. 가상환경 켜기
- (window) source venv/Scripts/activate
- (mac) source venv/bin/activate
<br/>

4. 필요한 모듈 설치
- pip install -r requirements.txt
<br/>


# 웹 구동

1. 웹 폴더로 이동
- cd IOT
<br/>

2. DB 생성(한 번만 해주면 됨)
- python manage.py makemigrations
- python manage.py migrate
<br/>

3. 서버 구동: 웹 실행시킬 때마다
- python manage.py runserver
<br/>

4. 링크 클릭
- 터미널 아래에서 두 번째 줄에 있는 "http://127.0.0.1:8000/" 를 "Ctrl + 마우스클릭"
<br/>

5. 웹 구동 완료
- 웹 크롤링(오늘의 메뉴)은 윈도우용 프로그램을 써서 맥에서는 작동하지 않습니다
<br/>

6. 웹 종료시: Ctrl + c
<br/>

# Modi 초음파 센서 구동

1. 모디 초음파 센서 USB 연결
<br/>

2. 터미널 하나 더 만들기
- 우측 하단 휴지통 아이콘 바로 왼쪽에 있는 분할 아이콘 클릭
<br/>

3. 실행(최상단 폴더에 있다는 전제하에 터미널에 입력)
- python congression.py
<br/>

4. 센서 작동 종료시: Ctrl + c
