# How to install?

it is strongly recommended that deploy via heroku.


## Cloning git & make heroku app

open terminal, and cd to folder you want to clone.

```
git clone https://github.com/DPS0340/DPSBot
```
and [install heroku CLI](https://devcenter.heroku.com/articles/heroku-cli#download-and-install). (if you haven't)

heroku login is needed.

```
heroku create (Your_app_name)
```
to make app.


## DB initialization guide

Please run following commands in your clone root folder:


```
heroku addons:create heroku-postgresql:hobby-dev -a (Your_app_name)
heroku pg:backups:restore 'https://github.com/DPS0340/DPSBot/raw/master/db-dump/backup.dump' DATABASE_URL -a (Your_app_name)
python3 ./db-init/db-init.py -url (Your_database_url)
```


![db-setup-heroku](https://github.com/DPS0340/DPSBot/blob/gh-pages/Screenshot_20181223_162448.png)
![db-init.py](https://github.com/DPS0340/DPSBot/blob/gh-pages/Screenshot_20181223_162448.png)

Process should be like this.

Required: token, prefix, your discord id, osuapikey, channel id to receive ticket


## First deploy to heroku

```
git push heroku master
```

**Now you've just deployed the app!**

Congratulations!

## Update bot

```
git pull origin master
git push heroku master
```
App is updated to latest version.

but, DPSBot updates very often. so may be unstable!

Please check build status!

[![Build Status](https://travis-ci.com/DPS0340/DPSBot.svg?branch=master)](https://travis-ci.com/DPS0340/DPSBot) 
