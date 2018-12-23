# DB initialization guide

Please run following commands in your clone root folder:

# if you use heroku

first, install [heroku postgres](https://elements.heroku.com/addons/heroku-postgresql) in your app.

```
heroku pg:backups:restore 'https://github.com/DPS0340/DPSBot/raw/master/db-dump/backup.dump' DATABASE_URL -a (Your_app_name)
python3 ./db-init/db-init.py -url (Your_database_url)
```


![db-setup-heroku](https://github.com/DPS0340/DPSBot/blob/gh-pages/Screenshot_20181223_162448.png)
![db-init.py](https://github.com/DPS0340/DPSBot/blob/gh-pages/Screenshot_20181223_162448.png)

process should be like this.

required: token, prefix, owner id, osuapikey, channel id to receive ticket
