from flask import Flask, jsonify
import socket
import os
import psycopg2
import sys
import logging
import json

class JsonFormatter(logging.Formatter):
    def format(self, record):
        return json.dumps({
            'severity': record.levelname,
            'message': record.getMessage(),
        })

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(JsonFormatter())
logging.getLogger().handlers = [handler]
logging.getLogger().setLevel(logging.INFO)


app = Flask(__name__)


@app.route('/')
def health():
    return jsonify(status='ok', hostname=socket.gethostname())


@app.route('/db-check')
def db_check():
    try:
        conn = psycopg2.connect(
            host=os.environ.get('DB_HOST'),
            database=os.environ.get('DB_NAME'),
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASSWORD')
        )
        cur = conn.cursor()
        cur.execute('SELECT 1')
        result = cur.fetchone()
        cur.close
        conn.close()
        return jsonify(status='ok', db='connected', result=result[0])
    except Exception as e:
        return jsonify(status='error', db='failed', message=str(e)), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
