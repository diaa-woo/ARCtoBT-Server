from flask import Flask, request, json
import subprocess
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return "뭐"

@app.route('/login', methods=['POST'])
def login():
    if len(request.get_data()) == 0:
        return 'null'
    params = json.loads(request.get_data(), encoding='utf-8')
    
    auth = open('auth.txt', 'r')
    if params['id']==auth.readline():
        return '성공!'
    else:
        return '?'

if __name__ == '__main__':
    wlan_address = subprocess.run(["hostname", "-I"], capture_output=True).stdout.decode().split()[0]     # hostname -I를 통해 파악 후, 상황에 따라 인덱스 값 변경
    app.run(host=wlan_address, debug=True)       