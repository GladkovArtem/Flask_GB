import os

from blog.app import app
from flask import render_template
from werkzeug.security import generate_password_hash
from blog.database import db


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        debug=True,
    )


# @app.cli.command("init-db")
# def init_db():
#     db.create_all()
#     print("done!")


@app.cli.command("create-admin")
def create_admin():
    """
    Run in your terminal:
    ➜ flask create-admin
    > created admin: <User #1 'admin'>
    """

    from blog.models import User
    admin = User(username="Admin", email="mail@mail.ru", is_staff=True)
    admin.password = os.environ.get("ADMIN_PASSWORD") or "adminpass"

    db.session.add(admin)
    db.session.commit()

    print("done! created admin:", admin)




