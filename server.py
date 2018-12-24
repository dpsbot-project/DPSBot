import json
import os
import sys
def server(id, lang="en_US"):
    return {'id':id, 'resistricted':False, 'language':lang}
def server_save(server:dict):
    with open('servers/%s.json' % server['id'], 'w') as w:
        json.dump(server, w)
def server_load(id):
    with open('servers/%s.json' % id, 'r') as r:
        return json.load(r)
def server_init(bot):
    for id in bot.server.id:
        if os.path.exists('servers/%s.json' % id):
            pass
        else:
            server_save(server(id))