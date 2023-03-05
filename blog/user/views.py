from flask import Blueprint, render_template
from werkzeug.exceptions import NotFound
from blog.models import User

users = Blueprint("users", __name__, url_prefix='/users', static_folder='../static')


@users.route('/')
def user_list():
    users = User.query.all()
    return render_template('users/list.html', users=users)


@users.route('/<int:user_id>/', endpoint="details")
def profile(user_id: int):
    user = User.query.filter_by(id=user_id).one_or_none()
    if users is None:
        raise NotFound(f"User #{user_id} doesn't exist!")

    return render_template('users/details.html', user=user)
