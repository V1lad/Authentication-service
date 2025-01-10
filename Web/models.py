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

    ownedToken = db.relationship('Token')
     
# Описывает сущность запись
class Token(db.Model):
    __tablename__ = 'tokens'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    
    parent_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    content = db.Column(db.String, default='')
    expiration_time = db.Column(db.Integer, default=0)
    
     # Корректно удаляет запись
    def delete(self, db):
        db.session.delete(self)
    