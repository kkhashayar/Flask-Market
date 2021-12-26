from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
# for hashing passwords: flask_bcrypt

from flask_login import LoginManager
from flask_bcrypt import Bcrypt


app = Flask(__name__)
#-- URI stands for uniform resource identifier
app.config["SQLALCHEMY_DATABASE_URI"] = #-- Your Database URI
app.config["DEBUG"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["SECRET_KEY"] = #-- Your secret key 
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.init_app(app) #-- to solve the current_user  is not defined problem
login_manager.login_view = "login"
login_manager.login_message_category = "info"

from market import routes
