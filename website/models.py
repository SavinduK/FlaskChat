from . import db
from sqlalchemy.sql import func


class Chatroom(db.Model):
 id = db.Column(db.Integer,primary_key=True)
 name = db.Column(db.String(75),unique=True)
 date_created =db.Column(db.DateTime(timezone=True),default=func.now()) 


class Message(db.Model):
 id = db.Column(db.Integer,primary_key=True)
 user_name = db.Column(db.String(75))
 chatroom_name = db.Column(db.String(75))
 message = db.Column(db.String(150))
 date_created =db.Column(db.DateTime(timezone=True),default=func.now())

