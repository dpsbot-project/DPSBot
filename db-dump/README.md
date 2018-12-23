# DB initialization guide

Please run following commands in your clone root folder:

# if you use heroku
```heroku pg:backups:restore 'https://github.com/DPS0340/DPSBot/raw/master/db-dump/backup.dump' DATABASE_URL -a (Your_app)```

```python db-init.py```
