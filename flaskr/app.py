from flaskext.mysql import MySQL
from flask import Flask
from point.blueprint import point

import json
  
# import credential
f = open('.credential')
credential = json.load(f)
f.close()

# create and configure the app
app = Flask(__name__) 

# Initial db
mysql_db = MySQL()
app.config['MYSQL_DATABASE_USER'] = credential['mysql']['user']
app.config['MYSQL_DATABASE_PASSWORD'] = credential['mysql']['password']
app.config['MYSQL_DATABASE_DB'] = credential['mysql']['db']
app.config['MYSQL_DATABASE_HOST'] = credential['mysql']['host']
mysql_db.init_app(app)
app.config['MYSQL_DB'] = mysql_db.connect()

# register blueprints
app.register_blueprint(point, url_prefix='/point/<customer_id>')
