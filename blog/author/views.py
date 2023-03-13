from flask import Blueprint, render_template
from blog.models import Author


authors = Blueprint("authors", __name__)


@authors.route("/")
def authors_list():
    authors = Author.query.all()
    return render_template("authors/list.html", authors=authors)
