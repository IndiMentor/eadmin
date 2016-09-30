from flask.ext.admin.contrib.peewee import ModelView
from peewee import Model, CharField, TextField, SmallIntegerField, SqliteDatabase
from flask_admin import Admin

db = SqliteDatabase('ems.db', check_same_thread=False)

class BaseModel(Model):
    class Meta:
        database = db

class Escort(BaseModel):
    """Defines an escort and the relationships she has with other entities
    Contains the following attributes:
    name            height      weight      hair_color  eyes
    vitals          bust        implants    tattoos     piercings   language
    brand_text      nationality ethnicity   description ad_text
    featured        available   vacation    new_girl    gfe
    pse             located_at

    null    index   unique  default
    """
    name = CharField(unique=True, max_length=80)
    height = CharField(null=True,max_length=10)
    weight = SmallIntegerField(null=True)
    hair_color = CharField(null=True, max_length=16)
    description = TextField(null=False)
    # eyes = CharField(null=True)
    # vitals = CharField(null=True)
    # bust = CharField(null=True)
    # implants = BooleanField(null=True)
    # tattoos = CharField(null=True,default=True)
    # piercings = CharField(null=True, default=False)
    # language = CharField(default='English')
    # brand_text = CharField()
    # nationality = CharField(null=True)
    # ethnicity = CharField(null=True)
    # ad_text = TextField()
    # # Flags
    # featured = BooleanField(default=False)
    # available = BooleanField(default=False)
    # vacation = BooleanField(default=False)
    # new_girl = BooleanField(default=True)
    # gfe = BooleanField(default=True)
    # pse = BooleanField(default=False)

    def __unicode__(self):
        return self.name


class EscortAdmin(ModelView):
    # Visible columns in the list view
    column_exclude_list = ['description']

    # List of columns that can be sorted. For 'user' column, use User.email as
    # a column.
    column_sortable_list = ('name', )

    # Full text search
    column_searchable_list = ('name', )

    # Column filters
    column_filters = ('name', )

    # form_ajax_refs = {
    #     'user': {
    #         'fields': (User.username, 'email')
    #     }
    # }


def init_admin(ems_admin_app):
    ems_admin = Admin(ems_admin_app,name='EMS',template_mode='bootstrap3')
    ems_admin.add_view(EscortAdmin(Escort))

    try:
        Escort.create_table(fail_silently=True)
    except:
        pass
