import argparse
import psycopg2

if __name__ == "__main__":
    token = input("Please type token.")
    prefix = input("Please type prefix.")
    osuapikey = input("Please type osu api key.")
    owner = input("Please type your discord id(Number).\nnot bot.")
    channel = input("Please type channel id to recieve ticket.")
    instruction = input("Please type bot introduce.")

    parser = argparse.ArgumentParser()
    parser.add_argument("-url", required=True)
    args = parser.parse_args()
    DATABASE_URL = args.url
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute("INSERT INTO settings VALUES('token', %s)" % token)
    cur.execute("INSERT INTO settings VALUES('prefix', %s)" % prefix)
    cur.execute("INSERT INTO settings VALUES('osuapikey', %s)" % osuapikey)
    cur.execute("INSERT INTO settings VALUES('owner', %s)" % owner)
    cur.execute("INSERT INTO settings VALUES('channel', %s)" % channel)
    cur.execute("INSERT INTO settings VALUES('instruction', %s)" % instruction)
    print("DB set up complete!")
    conn.exit()