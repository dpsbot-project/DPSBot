# DB initialization guide

Please run following commands in your clone root folder:

# if you use heroku
```
heroku pg:backups:restore 'https://github.com/DPS0340/DPSBot/raw/master/db-dump/backup.dump' DATABASE_URL -a (Your_app_name)
python3 ./db-init/db-init.py -url (Your_database_url)
```
![db-init.py](https://github.com/DPS0340/DPSBot/blob/gh-pages/Screenshot_20181223_162448.png)
required: token, prefix, owner id, osuapikey, channel id to receive ticket
