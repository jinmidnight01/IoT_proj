################ 환경 세팅 ################

# 가상환경 설치
python -m venv venv

# 가상환경 키기
(window) source venv/Scripts/activate
(mac) source venv/bin/activate

# 필요한 모듈 설치
pip install -r requirements.txt

################ 웹 구동 ################

# 웹 폴더로 이동
cd IOT

# DB 생성(한 번만 해주면 됨)
python manage.py makemigrations
python manage.py migrate

# 서버 구동: 웹 실행시킬 때마다
python manage.py runserver

# 링크 클릭
아래에서 두 번째 줄에 있는 "http://127.0.0.1:8000/" 를 "Ctrl + 마우스클릭"

# 완료

################ IoT 초음파 센서 구동 ################

# IoT 기기 연동
1. 모디 초음파 센서 USB 연결
2. 터미널 하나 더 만들기: 우측 하단 휴지통 아이콘 바로 왼쪽에 있는 분할 아이콘 클릭
3. 실행(최상단 폴더에 있다는 전제하에 터미널에 입력): python congression.py
