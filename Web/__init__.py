from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from json import loads
db = SQLAlchemy()
DB_NAME = "database.db"

# Создание приложения
def create_app():
    basedir = path.abspath(path.dirname(__file__))
           
    app = Flask(__name__)    
    # Конфигурируем базу данных
    with open("web/keys/secret_key.txt", "r") as file:
        app.config['SECRET_KEY'] = file.readline()
    app.config['SQLALCHEMY_DATABASE_URI'] =\
           'sqlite:///' + path.join(basedir, DB_NAME)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    with open("web/keys/jwt_secret_key.txt", "r") as file:
        app.config["JWT_SECRET_KEY"] = file.readline()
        
    db.init_app(app)
    jwt = JWTManager(app)
    # Подключаем чертежи из других файлов
    # from .views import views
    from .auth import auth
    # from .projects import projects
    
    # Регистрируем чертежи с соответственными адресами в приложении
    # app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    # app.register_blueprint(projects, url_prefix='/')

    # Подключаем модели для базы данных
    from .models import User

    create_database(app)
    
    return app


def create_database(app):
    with app.app_context():
        db.create_all()

