from flask import redirect, url_for
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_bcrypt import generate_password_hash
from flask_login import current_user

from blog.forms import user
from blog.models import Tag, Articles, User
from blog.database import db


class MyAdminIndexView(AdminIndexView):

    @expose("/")
    def index(self):
        if not (current_user.is_authenticated and current_user.is_staff):
            return redirect(url_for("auth.login"))
        return super().index()


# Create admin with custom base template
admin = Admin(
    name="Blog Admin",
    index_view=MyAdminIndexView(),
    template_mode="bootstrap4",
)


# Customized admin interface
class CustomView(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_staff

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("auth.login"))


class TagAdminView(CustomView):
    column_searchable_list = ("name",)
    column_filters = ("name",)
    can_export = True
    export_types = ["csv", "xlsx"]
    create_modal = True
    edit_modal = True


class UserAdminView(CustomView):
    column_exclude_list = ("password_",)
    column_details_exclude_list = ("password_",)
    column_searchable_list = ("first_name", "last_name", "username", "is_staff", "email")
    column_filters = ("first_name", "last_name", "username", "is_staff", "email")
    can_create = False
    can_edit = True
    can_delete = False
    column_editable_list = ("first_name", "last_name", "is_staff")


class ArticlesAdminView(CustomView):
    column_searchable_list = ("title",)
    column_filters = ("title",)
    can_export = True
    export_types = ["csv", "xlsx"]
    can_create = False

# Add views
admin.add_view(UserAdminView(User, db.session, category="Models"))
admin.add_view(ArticlesAdminView(Articles, db.session, category="Models"))
admin.add_view(TagAdminView(Tag, db.session, category="Models"))





