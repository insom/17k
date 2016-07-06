from __future__ import with_statement
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, Blueprint
import sys
import hashlib
import os.path
import requests
import json
import os
from cStringIO import StringIO

app = Flask(__name__)

PPL = {
    's': 'insom',
    'n': 'iweb',
    'b': 'balloz',
}

def upload_to_storage(host, space, username, password, f):
    tokurl = 'https://%s.iweb-storage.com/jsapi/spaces/%s/files/' % (host, space)
    x = requests.get(tokurl, auth=(username, password))
    tok = json.loads(x.content)['uploadToken']
    url = 'https://%s.iweb-storage.com/upload?t=%s' % (host, tok)
    id = hashlib.md5(tok).hexdigest()[:8]
    files = {'file': ('%s.png' % id, f)}
    r = requests.post(url, files=files)
    url = 'http://%s.iweb-storage.com/public/files/%s.png?inline=1' % (host, id)
    x = 'x'
    for k, v in PPL.items():
        if v == host:
            x = k
    return 'http://17k.uk/%s/%s.png' % (x, id)

@app.route('/<i>/<hash_>')
def image_shortened(i, hash_):
    url = 'http://%s.iweb-storage.com/public/files/%s?inline=1' % (PPL[i], hash_)
    return redirect(url)

@app.route('/scrup/<username>/', methods=['POST'])
def handle(username):
    f = StringIO(request.data)
    host = username.split('-')[0]
    url = upload_to_storage(host, 'Public', username, request.args.get('password'), f)
    return url, 201

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 6525))
    app.run(host='127.0.0.1', port=port)
