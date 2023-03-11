from blog.app import app
from flask import render_template
from werkzeug.security import generate_password_hash
from blog.database import db


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        debug=True,
    )


@app.cli.command("init-db")
def init_db():
    db.create_all()
    print("done!")


@app.cli.command("create-users")
def create_users():
    """
    Run in your terminal:
    flask create-users
    > done! created users: <User #1 'admin'> <User #2 'james'>
    """

    from blog.models import User
    admin = User(username="superadmin", email="artem@mail.ru", password=generate_password_hash('Qwerty12345'), is_staff=True)

    db.session.add(admin)
    db.session.commit()

    print("done! created users:", admin)




