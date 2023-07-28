from flask import Flask, request, json
import subprocess
import string
import random

app = Flask(__name__)

_LENGTH = 10

def _check_auth(auth_key):
    db = open('db.txt', 'r')
    if auth_key in db.read() :
        db.close()
        return True
    
    db.close()
    return False

def _pass_auth() :
    # Auth part
    if len(request.get_data()) == 0 : return 'Login First!!'
    else:
        keys = json.loads(request.get_data(), encoding='utf-8')
        if not _check_auth(keys['key']) : return 'Key fails'
    return 0

@app.route('/')
def index():
    return "뭐"

@app.route('/login', methods=['POST'])
def login():
    db = open('db.txt', 'a')
    if len(request.get_data()) == 0:
        return 'null'
    params = json.loads(request.get_data(), encoding='utf-8')
    
    print(params)

    if params['id']==_PW:
        string_pool = string.ascii_letters
        key = ""
        for i in range(_LENGTH):
            key += random.choice(string_pool)
        db.write(key+'\n')
        db.close()
        return key
    else:
        db.close()
        return '?'


if __name__ == '__main__':
    db = open('db.txt', 'w')
    db.close()

    auth = open('auth.txt', 'r')
    _PW = auth.readline()
    auth.close()

    wlan_address = subprocess.run(["hostname", "-I"], capture_output=True).stdout.decode().split()[0]     # hostname -I를 통해 파악 후, 상황에 따라 인덱스 값 변경
    app.run(host=wlan_address, debug=True)       