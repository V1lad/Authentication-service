from . import db
from flask_login import UserMixin

# Описывает сущность пользователь
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    email = db.Column(db.String(150), unique=True)
    firstName = db.Column(db.String(150), default='')
    password = db.Column(db.String(150))
    
    projectsAuthInfo = db.Column(db.JSON, default='{}')

     
    