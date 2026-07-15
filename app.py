from flask import Flask, jsonify
import socket

app = Flask(__name__)

@app.route('/')
def health():
    return jsonify(status = 'ok', hostname = socket.gethostname())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)