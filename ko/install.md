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
cd DPSBot
pip install -r requirements.txt
```


## DB 설치

```
sudo apt update
sudo apt install postgresql postgresql-contrib
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
계정을 다시 바꾸기 위해서  비밀번호를 입력하세요.
```
export DATABASE_URL=postgres://postgres@localhost/DPSBot
sudo nano ~/.bashrc
```
```
export DATABASE_URL=postgres://postgres@localhost/DPSBot
```

라고 쓰세요.

## DB 초기화

```
cd DPSBot
python3 ./db-init/db-init.py -url postgres://postgres@localhost/DPSBot
pg_restore --dbname=DPSBot -U postgres db-dump.backup.dump
```


## 봇 배포

```
python3 Main.py &
```


## 시작시 자동 실행

```
crontab -e
```

파일의 끝에 쓰세요.
```
@reboot python (클론한_경로)/DPSBot/Main.py &
```


## 봇 업데이트

```
git pull origin master
```
봇이 최신 버전으로 업데이트 되었습니다.

다만, DPSBot은 자주 업데이트 되어서 불안정할 수 있습니다.

빌드 상태를 확인하세요!

[![Build Status](https://travis-ci.com/DPS0340/DPSBot.svg?branch=master)](https://travis-ci.com/DPS0340/DPSBot) 
