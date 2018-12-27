import argparse
import psycopg2
import os

if __name__ == "__main__":
    token = input("Please type token.")
    prefix = input("Please type prefix.")
    osuapikey = input("Please type osu api key.")
    owner = input("Please type your discord id(Number).\nnot bot.")
    channel = input("Please type channel id to recieve ticket.")
    parser = argparse.ArgumentParser()
    parser.add_argument("-url", required=True)
    args = parser.parse_args()
    DATABASE_URL = args.url
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute("INSERT INTO settings VALUES('token', '%s') ON CONFLICT (name) DO UPDATE SET name='token', body='%s'" % (token, token))
    cur.execute("INSERT INTO settings VALUES('prefix', '%s') ON CONFLICT (name) DO UPDATE SET name='prefix', body='%s'" % (prefix, prefix))
    cur.execute("INSERT INTO settings VALUES('osuapikey', '%s') ON CONFLICT (name) DO UPDATE SET name='osuapikey', body='%s'" % (osuapikey, osuapikey))
    cur.execute("INSERT INTO settings VALUES('owner', '%s') ON CONFLICT (name) DO UPDATE SET name='owner', body='%s'" % (owner, owner))
    cur.execute("INSERT INTO settings VALUES('channel', '%s') ON CONFLICT (name) DO UPDATE SET name='channel', body='%s'" % (channel, channel))
    cur.execute("INSERT INTO settings VALUES('instructions', 'a open source bot.') ON CONFLICT (name) DO UPDATE SET name='instructions', body='a open source bot.'")
    conn.close()
    os.system("export DPSBOT_URL=%s" % DATABASE_URL)
    os.system('echo "export DPSBOT_URL=%s" >> $HOME/.bashrc' % DATABASE_URL)
    print("DB set up complete!")
