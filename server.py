from flask import Flask
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return "뭐"

if __name__ == '__main__':
    wlan_address = subprocess.check_output(["hostname", "-I"]).decode().split()[0]      # hostname -I를 통해 파악 후, 상황에 따라 인덱스 값 변경
    app.run(host=wlan_address, debug=True)       