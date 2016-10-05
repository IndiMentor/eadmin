"""Main entry point for app and all app initialization"""
from flask import Flask, redirect
import logging
from peewee import SqliteDatabase
from flask_basicauth import BasicAuth
from init_admin import init_admin

import flask_admin

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

ems_admin_app = Flask(__name__)
ems_admin_app.config['SECRET_KEY'] = '123456790'
db = SqliteDatabase('ems.db', check_same_thread=False)
ems_admin_app.config['BASIC_AUTH_USERNAME'] = 'john'
ems_admin_app.config['BASIC_AUTH_PASSWORD'] = 'matrix'
ems_admin_app.config['BASIC_AUTH_FORCE'] = True
basic_auth = BasicAuth(ems_admin_app)


@ems_admin_app.route('/')
def index():
    return home_page()
    #return redirect('/admin/')
    # for rate in range(300,190,-10):
    #     new_rate=Rate(rate)
    #     new_rate.indi_vip(disc=20)

    return '<a href="/admin/">Click me to get to Admin!</a>'

if __name__ == '__main__':
    init_admin(ems_admin_app, db=db)
    ems_admin_app.run(debug=False)
