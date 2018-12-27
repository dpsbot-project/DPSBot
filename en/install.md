# How to install?

deploy via Heroku or ubuntu server.

# Deploy via heroku

## Cloning git & make heroku app

open terminal, and cd to folder you want to clone.

```
git clone https://github.com/DPS0340/DPSBot
cd DPSBot
```
and [install heroku CLI](https://devcenter.heroku.com/articles/heroku-cli#download-and-install). (if you haven't)

heroku login is needed.

```
heroku create (Your_app_name)
```
to make app.


## DB initialization


```
heroku addons:create heroku-postgresql:hobby-dev -a (Your_app_name)
heroku addons:create heroku-redis:hobby-dev -a (Your_app_name)
heroku pg:backups:restore 'https://github.com/DPS0340/DPSBot/raw/master/db-dump/backup.dump' DATABASE_URL -a (Your_app_name)
heroku run python ./db-init/db-init.py -url (Your_database_url)
```
and go heroku dashboard, set the variable 'DPSBOT_URL' to your DATABASE_URL

![db-setup-heroku](https://github.com/DPS0340/DPSBot/blob/gh-pages/Screenshot_20181223_162759.png)
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

but, DPSBot is updated very often. so may be unstable!

Please check build status!

[![Build Status](https://travis-ci.com/DPS0340/DPSBot.svg?branch=master)](https://travis-ci.com/DPS0340/DPSBot) 


# install your own ubuntu server

## Cloning git & install dependencies


```
git clone https://github.com/DPS0340/DPSBot
sudo apt install python3 python3-pip
cd DPSBot
pip3 install -r requirements.txt
```


## Setting up DB

```
sudo apt install postgresql postgresql-client postgresql-contrib
sudo nano /etc/postgresql/10/main/pg_hba.conf
```
change this:
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
to
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
then
```
sudo service postgresql restart
```

## create database
```
su - postgres
```
press enter
```
createdb DPSBot
su - (your username)
```
then type your password to change account.
```


## DB initialization

```
cd DPSBot
pg_restore -x -d DPSBot --no-acl -U postgres --host=localhost db-dump/backup.dump  # ignore errors
python3 ./db-init/db-init.py -url postgres://postgres@localhost/DPSBot
```


## Deploy bot

```
python3 Main.py &
```
deploy complete!


## Always run in startup

```
crontab -e
```

write at file's end.
```
@reboot python3 (clone_path)/DPSBot/Main.py &
```


## Update bot

```
git pull origin master
```
App is updated to latest version.

but, DPSBot is updated very often. so may be unstable!

Please check build status!

[![Build Status](https://travis-ci.com/DPS0340/DPSBot.svg?branch=master)](https://travis-ci.com/DPS0340/DPSBot) 
