"""Main entry point for app and all app initialization"""
from flask import Flask
import logging
from models import init_admin

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)



ems_admin_app = Flask(__name__)
ems_admin_app.config['SECRET_KEY'] = '123456790'



@ems_admin_app.route('/')
def index():
    return '<a href="/admin/">Click me to get to Admin!</a>'

if __name__ == '__main__':
    init_admin(ems_admin_app)
    ems_admin_app.run(debug=True)