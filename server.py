from flask import Flask, request, json
import subprocess
import string
import random
import time
from Bluetoothctl import Bluetoothctl

app = Flask(__name__)

_LENGTH = 10

#*Index---------------------------------------
@app.route('/')
def index():
    return "뭐"
#---------------------------------------------

#*Auth part-----------------------------------
def _check_auth(auth_key):
    db = open('db.txt', 'r')
    if auth_key in db.read() :
        db.close()
        return True
    
    db.close()
    return False

def _pass_auth() :
    if len(request.get_data()) == 0 : return 'Login First!!'
    else:
        keys = json.loads(request.get_data())
        if not _check_auth(keys['key']) : return 'Key fails'
    return 0

@app.route('/login', methods=['POST'])
def login():
    db = open('db.txt', 'a')
    if len(request.get_data()) == 0:
        return 'null'
    params = json.loads(request.get_data())
    
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
#----------------------------------------------

#*Bluetooth control----------------------------
@app.route('/paired', methods=['POST'])
def paired():
    result = _pass_auth()
    if result != 0 : return result

    return paireds

@app.route('/scan', methods=['POST'])
def scan():
    result = _pass_auth()
    if result != 0 : return result

    bl.start_scan()
    time.sleep(5)
    discoverables = bl.get_discoverable_devices()
    return discoverables

@app.route('/connect', methods=['POST'])
def connect():
    global paireds

    result = _pass_auth()
    if result != 0 : return result

    mac_addr = json.loads(request.get_data())['mac_addr']
    for device in paireds:
        if device["mac_address"] == mac_addr : 
            bl.connect(mac_addr)
            return "Done!"
    
    result = bl.pair(mac_addr)
    if result == False : bl.connect(mac_addr)
    return "Um"

@app.route('/disconnect', methods=['POST'])
def disconnect():
    result = _pass_auth()
    if result != 0 : return result
    
    mac_addr = json.loads(request.get_data())['mac_addr']
    status = bl.disconnect(mac_addr)

    if status == False : return "Fail"
    return "Done!"
#----------------------------------------------

if __name__ == '__main__':
    bl = Bluetoothctl()
    paireds = bl.get_paired_devices()

    db = open('db.txt', 'w')
    db.close()

    auth = open('auth.txt', 'r')
    _PW = auth.readline()
    auth.close()

    wlan_address = subprocess.run(["hostname", "-I"], capture_output=True).stdout.decode().split()[0]     # hostname -I를 통해 파악 후, 상황에 따라 인덱스 값 변경
    app.run(host=wlan_address, debug=True)       