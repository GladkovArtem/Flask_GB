from time import time

from flask import Flask, g
from flask import request

app = Flask(__name__)

count = 0

@app.route('/', methods=['GET'])
def index():
    name = request.args.get('name', None)
    global count
    count += 1
    return f'Количество посещений: {count}!'

@app.before_request
def process_before_request():
    g.start_time = time()

@app.after_request
def process_after_request(response):
    if hasattr(g, "start_time"):
        response.headers["process-time"] = time() - g.start_time

    return response


@app.errorhandler(404)
def handler_404(error):
    return '404'
