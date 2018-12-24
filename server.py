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
    for server.id in bot.servers:
        if os.path.exists('servers/%s.json' % server.id):
            pass
        else:
            server_save(server(server.id))