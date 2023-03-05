from blog.articles.views import articles
from blog.user.views import users
from flask import Flask, render_template
from blog.database import db
from blog.auth.views import login_manager, auth


app = Flask(__name__)
app.register_blueprint(users, url_prefix="/users")
app.register_blueprint(articles, url_prefix="/articles")
app.register_blueprint(auth, url_prefix="/auth")
app.config['SECRET_KEY'] = '_qv3585a9i^w0dgdtcmj$osrna24$@+pzs5ga%h#efp&()mxg1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////db.sqlite'
login_manager.init_app(app)
db.init_app(app)


@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")
