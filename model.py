from emsadmin import db
from peewee import (CharField, TextField, SmallIntegerField,  BooleanField,
                    PrimaryKeyField, ForeignKeyField)
from peewee import Model

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
    # Keys
    user_id = PrimaryKeyField()
    site_id = ForeignKeyField(models.site.Site, related_name="works_for")

    # Important Fields
    name = CharField(unique=True, max_length=80)

    # Frequently Updated Fields
    base_rate = SmallIntegerField(null=True)
    brand_text = CharField()
    ad_text = TextField(null=True)
    description = TextField(null=False)
    on_today = BooleanField(null=True, default=False)
    on_tommorrow = BooleanField(null=True, default=False)
    available_text = CharField(null=True, max_length=64)
    vacation = BooleanField(null=True, default=False)

    height = CharField(null=True, max_length=10)
    weight = SmallIntegerField(null=True)
    hair_color = CharField(null=True, max_length=16)
    eyes = CharField(null=True)
    vitals = CharField(null=True)
    bust = CharField(null=True)

    implants = BooleanField(null=True)
    tattoos = CharField(null=True, default=True)
    piercings = CharField(null=True, default=False)

    language = CharField(null=True, default='English')
    nationality = CharField(null=True)
    ethnicity = CharField(null=True)

    # Flags
    featured = BooleanField(null=True, default=False)

    new_girl = BooleanField(null=True, default=True)
    gfe = BooleanField(null=True, default=True)
    pse = BooleanField(null=True, default=False)

    def set_on_today(self, status):
        self.on_today = status

    def set_on_tommorrow(self, status):
        self.on_tommorrow = status

    def __unicode__(self):
        return self.name



class Location(BaseModel):
    name = CharField(unique=True, max_length=40)
    description = CharField(max_length=80)
    directions = CharField(null=True, max_length=80)
    is_incall = BooleanField(null=True, default=False)
    active = BooleanField(default=True, null=True)

    def __unicode__(self):
        return self.name


class Site(BaseModel):
    site_id = PrimaryKeyField()
    name = CharField(unique=True, max_length=32)
    seo_text = CharField(max_length=64)
    tag_line = CharField(max_length=64)

    # Marketing Stuff
    logo = CharField(max_length=255,null=True, default=None)
    # logo2 = ForeignKeyField(Photo, related_name='is logo of', null=True, default=None)
    banner = CharField(max_length=255,null=True, default=None)
        # ForeignKeyField(Photo, 'is banner for', null=True, default=None)

    # Contact Info
    booking_email = CharField(null=True)
    admin_email = CharField(null=True)
    phone_1 = CharField(null=True)
    phone_2 = CharField(null=True)
    phone_3 = CharField(null=True)

    base_rate = SmallIntegerField(null=True)
    discount_amt = SmallIntegerField()

    def __unicode__(self):
        return self.name


class Photo(BaseModel):
    image_id = PrimaryKeyField()
    name = CharField(null=False, max_length=255)
    path = CharField(null=False, max_length=255)

    def __unicode__(self):
        return self.name
