from time import time
from blog.views.users import users_app
from blog.views.articles import articles_app
from flask import Flask, g, render_template
from flask import request


app = Flask(__name__)
count = 0
app.register_blueprint(users_app, url_prefix="/users")
app.register_blueprint(articles_app, url_prefix="/articles")


@app.route('/', methods=['GET'])
def index():
    # name = request.args.get('name', None)
    # global count
    # count += 1
    # return f'Количество посещений: {count}!'
    return render_template("index.html")


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