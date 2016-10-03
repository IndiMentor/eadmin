"""Model for files / images"""
from emsadmin import db
from .base import BaseModel
from peewee import Model, PrimaryKeyField, TextField, CharField
from flask_admin.contrib.peewee import ModelView


class Photo(BaseModel):
    image_id = PrimaryKeyField()
    photo_name = CharField(null=False, max_length=128)
    photo_path = CharField(null=False, max_length=255)

    def __unicode__(self):
        return self.name


def create_fake_photos(db):
    return
