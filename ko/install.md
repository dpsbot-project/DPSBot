# 어떻게 설치하나요?

heroku 또는 우분투 서버를 사용해서 배포하세요.

# heroku를 통한 배포

## git 복제 & heroku 앱 만들기

터미널을 열고, git을 복제할 위치로 이동하세요.

```
git clone https://github.com/DPS0340/DPSBot
cd DPSBot
```
heroku CLI가 없다면 [설치](https://devcenter.heroku.com/articles/heroku-cli#download-and-install)하세요.

heroku 로그인이 필요합니다.

```
heroku create (앱_이름)
```
앱을 만듭니다.

## DB 초기화 가이드

클론의 root 폴더에 다음 명령을 실행하세요.


```
heroku addons:create heroku-postgresql:hobby-dev -a (앱_이름)
heroku pg:backups:restore 'https://github.com/DPS0340/DPSBot/raw/master/db-dump/backup.dump' DATABASE_URL -a (앱_이름)
python3 ./db-init/db-init.py -url (데이터베이스_url)
```


![db-setup-heroku](https://github.com/DPS0340/DPSBot/blob/gh-pages/Screenshot_20181223_162759.png)
![db-init.py](https://github.com/DPS0340/DPSBot/blob/gh-pages/Screenshot_20181223_162448.png)

과정이 이렇게 되어야 합니다.

토큰, 접두사, 당신의 디스코드 id, osu api 키, 건의를 받을 채널 id가 필요합니다.


## heroku의 첫번째 배포

```
git push heroku master
```

**이제 당신은 방금 앱을 배포하셨습니다!**

축하드립니다!

## 봇 업데이트

```
git pull origin master
git push heroku master
```
봇이 최신 버전으로 업데이트 되었습니다.

다만, DPSBot은 자주 업데이트 되어서 불안정할 수 있습니다.

빌드 상태를 확인하세요!

[![Build Status](https://travis-ci.com/DPS0340/DPSBot.svg?branch=master)](https://travis-ci.com/DPS0340/DPSBot) 


# 우분투 서버에 설치하기

## git 클론 & 의존성 설치


```
git clone https://github.com/DPS0340/DPSBot
sudo apt install python3 python3-pip
cd DPSBot
pip3 install -r requirements.txt
```


## DB 설치

```
sudo apt install postgresql postgresql-client postgresql-contrib
sudo nano /etc/postgresql/10/main/pg_hba.conf
```
이것을
```
# "local" is for Unix domain socket connections only
local   all             all                                     peer
# IPv4 local connections:
host    all             all             127.0.0.1/32            md5
# IPv6 local connections:
host    all             all             ::1/128                 md5
# Allow replication connections from localhost, by a user with the
# replication privilege.
local   replication     all                                     peer
host    replication     all             127.0.0.1/32            md5
host    replication     all             ::1/128                 md5
```
```
# "local" is for Unix domain socket connections only
local   all             all                                     trust
# IPv4 local connections:
host    all             all             127.0.0.1/32            trust
# IPv6 local connections:
host    all             all             ::1/128                 trust
# Allow replication connections from localhost, by a user with the
# replication privilege.
local   replication     all                                     trust
host    replication     all             127.0.0.1/32            trust
host    replication     all             ::1/128                 trust
```
이렇게 바꾸세요.

그리고
```
sudo service postgresql restart
```

## DATABASE_URL 변수 설정

```
su - postgres
```
엔터를 누르세요.
```
createdb DPSBot
su - (your username)
```
계정을 다시 바꾸기 위해 비밀번호를 입력하세요.


## DB initialization

```
cd DPSBot
pg_restore -x -d DPSBot --no-acl -U postgres --host=localhost db-dump/backup.dump  # 오류 무시
python3 ./db-init/db-init.py -url postgres://postgres@localhost/DPSBot
```


## 봇 배포

```
python3 Main.py &
```
배포 완료!


## 시작시 자동 실행

```
crontab -e
```

파일의 끝에 쓰세요.
```
@reboot python3 (클론한_경로)/DPSBot/Main.py &
```


## 봇 업데이트

```
git pull origin master
```
봇이 최신 버전으로 업데이트 되었습니다.

다만, DPSBot은 자주 업데이트 되어서 불안정할 수 있습니다.

빌드 상태를 확인하세요!

[![Build Status](https://travis-ci.com/DPS0340/DPSBot.svg?branch=master)](https://travis-ci.com/DPS0340/DPSBot) 