from emsadmin import db
from peewee import Model
from flask_admin.contrib.peewee import ModelView


class BaseModel(Model):
    class Meta:
        database = db


class BaseModelView(ModelView):  # https://flask-admin.readthedocs.io/en/latest/api/mod_model/
    can_delete = False  # disable model deletion
    page_size = 50  # the number of entries to display on the list view

    # Dictionary where key is column name and value is string to display.
    # column_labels = dict(name='Name', last_name='Last Name')

    # Dictionary where key is column name and value is description for list view column or add/edit formfield
    # column_descriptions = dict(full_name='First and Last name')

    # Dictionary of list view column formatters.
    # For example, if you want to show price multiplied by two, you can do something like this:
    # column_formatters = dict(price=lambda v, c, m, p: m.price*2)

    # column_default_sort = None
    # Default sort column if no sorting is applied.
    # column_default_sort = 'user'
