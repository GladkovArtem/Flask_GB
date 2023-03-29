from blog.articles.views import articles_app
from blog.author.views import authors
from blog.configs import DevConfig
from blog.database import db
from blog.user.views import users
from flask import Flask, render_template
from blog.auth.views import login_manager, auth
import os
from flask_migrate import Migrate
from blog.security import flask_bcrypt
from blog.admin.admin import admin
from blog.api import init_api


app = Flask(__name__)
app.config.from_object(DevConfig)
app.register_blueprint(users, url_prefix="/users")
app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(articles_app, url_prefix="/articles")
app.register_blueprint(authors, url_prefix="/authors")
# app.config['SECRET_KEY'] = '_qv3585a9i^w0dgdtcmj$osrna24$@+pzs5ga%h#efp&()mxg1'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# file_path = os.path.abspath(os.getcwd()) + "\database.db"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + file_path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////db.sqlite'
login_manager.init_app(app)
db.init_app(app)
migrate = Migrate(app, db, compare_type=True)
flask_bcrypt.init_app(app)
admin.init_app(app)
api = init_api(app)


@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")


@app.cli.command("create-tags")
def create_tags():
    """
    Run in your terminal:    ➜ flask create-tags
    """
    from blog.models import Tag
    for name in [
        "flask",
        "django",
        "python",
        "sqlalchemy",
        "news",
    ]:
        tag = Tag(name=name)
        db.session.add(tag)
    db.session.commit()
    print("created tags")
