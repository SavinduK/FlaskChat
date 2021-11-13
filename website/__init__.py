from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
DB_NAME ="database.db"

#-------------------------------------------------------------------------
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "@ABC#123"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    csrf  = CSRFProtect(app)

    from .views import views
    from .models import Chatroom,Message
    create_database(app)
    csrf.exempt(views)
    app.register_blueprint(views,url_prefix="/")


    return app
#---------------------------------------------------------------------------
def create_database(app):
 if not path.exists("website/"+DB_NAME):
  db.create_all(app=app)
  print("Database Created")
