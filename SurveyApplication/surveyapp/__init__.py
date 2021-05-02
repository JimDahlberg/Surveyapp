from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

#creates the app and configs
app = Flask(__name__)
app.config['SECRET_KEY'] = b'\xe4\x90\x1a\x02\xdf\xd0\x7fj\x08\x8b\xa0\xb9!NI&'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
loginManager = LoginManager(app)

from surveyapp import routes
