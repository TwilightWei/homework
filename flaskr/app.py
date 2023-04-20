from base64 import b64decode
from flaskext.mysql import MySQL
from flask import Flask
from blueprint.account.views import account

import json
import logging

# Create and configure the app
app = Flask(__name__)

# Config logger
logging.basicConfig(level = logging.INFO)

# Import credential
with open('.credential') as f:
    credential = json.load(f)

# Initial vars
app.config['PASSWORD_SALT'] = b64decode(credential['password_salt'].encode('utf-8'))

# Initial db
mysql_db = MySQL()
app.config['MYSQL_DATABASE_USER'] = credential['mysql']['user']
app.config['MYSQL_DATABASE_PASSWORD'] = credential['mysql']['password']
app.config['MYSQL_DATABASE_DB'] = credential['mysql']['db']
app.config['MYSQL_DATABASE_HOST'] = credential['mysql']['host']
mysql_db.init_app(app)
app.config['MYSQL_DB'] = mysql_db.connect()

# register blueprints
app.register_blueprint(account, url_prefix='/account')