# 어떻게 설치하나요?

heroku를 통한 배포가 강력하게 추천됩니다..


## git 복제 & heroku 앱 만들기

터미널을 열고, git을 복제할 위치로 이동하세요.

```
git clone https://github.com/DPS0340/DPSBot
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


![db-setup-heroku](https://github.com/DPS0340/DPSBot/blob/gh-pages/Screenshot_20181223_162448.png)
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
앱이 최신 버전으로 업데이트 되었습니다.
