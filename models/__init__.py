"""All of the database models from what I understand this will consolidate the
imports
"""
from flask_admin import Admin
from .escort import Escort, EscortAdmin, create_fake_escorts
from .location import Location, LocationAdmin, create_fake_locations
from .site import Site, SiteAdmin, create_fake_sites
from .photo import Photo, create_fake_photos
from peewee import IntegrityError


__author__ = 'eljefeloco'


def init_admin(ems_admin_app, db):
    ems_admin = Admin(ems_admin_app, name='EMS', template_mode='bootstrap3')
    ems_admin.add_view(EscortAdmin(Escort))
    ems_admin.add_view(LocationAdmin(Location))
    ems_admin.add_view(SiteAdmin(Site))

    Photo.create_table(fail_silently=True)
    create_fake_photos(db)

    Site.create_table(fail_silently=True)
    create_fake_sites(db)

    Location.create_table(fail_silently=True)
    create_fake_locations(db)

    Escort.create_table(fail_silently=True)
    create_fake_escorts(db)
