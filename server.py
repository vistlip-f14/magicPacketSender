from flask import Flask, render_template, request
import requests
import socket
import struct
from traceback import print_exc

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
DEFAULT_PORT = 7

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/magic')
def send_magic():
    mac_addr = request.args.get("mac_address")
    try:
        send_magic_packet(mac_addr)
 
    except BaseException:
        print_exc()
        return render_template('index.html'), 500
    
    return render_template('index.html')


def send_magic_packet(addr):
    # create socket
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        # parse address
        mac_ = addr.upper().replace("-", "").replace(":", "")
        if len(mac_) != 12:
            raise Exception("invalid MAC address format: {}".format(addr))
        buf_ = b'f' * 12 + (mac_ * 20).encode()
        # encode to magic packet payload
        magicp = b''
        for i in range(0, len(buf_), 2):
            magicp += struct.pack('B', int(buf_[i:i + 2], 16))
 
        # send magic packet
        print("sending magic packet for: {}".format(addr))
        s.sendto(magicp, ('<broadcast>', DEFAULT_PORT))
 
 
if __name__ == "__main__":
    app.run("0.0.0.0", port=8080, debug=False)