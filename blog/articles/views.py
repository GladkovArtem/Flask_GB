from flask import Blueprint, render_template, request, current_app, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from werkzeug.exceptions import NotFound
from blog.models import Articles, Author, Tag
from blog.models import db
from blog.forms.article import CreateArticleForm


articles_app = Blueprint("articles_app", __name__, url_prefix='/articles', static_folder='../static')


@articles_app.route('/')
def articles_list():
    articles = Articles.query.all()
    return render_template("articles_app/list.html", articles=articles)


@articles_app.route("/<int:article_id>/", endpoint="details")
def article_details(article_id):
    articles = Articles.query.filter_by(id=article_id).options(
        joinedload(Articles.tags)   # для подгрузки тегов
    ).one_or_none()
    if articles is None:
        raise NotFound(f"Article #{article_id} doesn't exist!")

    return render_template('articles_app/details.html', articles=articles)


@articles_app.route("/create/", methods=["GET", "POST"], endpoint="create")
@login_required
def create_article():
    error = None
    form = CreateArticleForm(request.form)
    form.tags.choices = [(tag.id, tag.name) for tag in Tag.query.order_by("name")]
    if request.method == "POST" and form.validate_on_submit():
        articles = Articles(title=form.title.data.strip(), body=form.body.data)
        db.session.add(articles)
        if form.tags.data:  # если в форму были переданы теги
            selected_tags = Tag.query.filter(Tag.id.in_(form.tags.data))
            for tag in selected_tags:
                articles.tags.append(tag)  # добавляем выбранные теги к статье
        if current_user.author:
            # use existing author if present
            articles.author = current_user.author
        else:
            # otherwise create author record
            author = Author(user_id=current_user.id)
            db.session.add(author)
            db.session.flush()
            articles.author = current_user.author

        try:
            db.session.commit()
        except IntegrityError:
            current_app.logger.exception("Could not create a new article!")
            error = "Could not create article!"
        else:
            return redirect(url_for("articles_app.details", article_id=articles.id))
    return render_template("articles_app/create.html", form=form, error=error)
