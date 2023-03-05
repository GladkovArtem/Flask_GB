from flask import Blueprint, render_template
from werkzeug.exceptions import NotFound
from blog.models import Articles


articles = Blueprint("articles", __name__, url_prefix='/articles', static_folder='../static')


@articles.route('/')
def articles_list():
    articles = Articles.query.all()
    return render_template("articles/list.html", articles=articles)


@articles.route("/<string:title>/", endpoint="details")
def article_details(title):
    title = Articles.query.filter_by(id=title).one_or_none()
    if articles is None:
        raise NotFound(f"Article #{title} doesn't exist!")

    return render_template('articles/details.html', title=title)
