from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from .models import User
from . import db
import bcrypt
from flask_jwt_extended import create_access_token, verify_jwt_in_request, get_jwt_identity

auth = Blueprint('auth', __name__)

# Отвечает за регистрацию
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == "POST":
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('Аккаунт с такой почтой уже существует', category='error')
        elif len(email) < 4:
            flash("Почтовый адрес должен быть длиннее 4 символов", category="error")
        elif len(firstName) < 2:
            flash("Имя должно состоять хотя бы из одного символа", category="error")
        elif password1 != password2:
            flash("Пароли не совпадают", category="error")
        elif len(password1) < 7:
            flash("Пароль должен быть длиннее 7 символов", category="error")
        else:
            new_user = User(email=email, firstName=firstName, password=password1)

            db.session.add(new_user)
            db.session.commit()
            flash("Аккаунт создан", category="success")
            return redirect(url_for('auth.login'))
        
    return render_template("sign_up.html")

@auth.route('/get_token', methods=['POST'])
def get_token():
    info = request.json
    user = User.query.filter_by(email=info["email"]).first()
    if user and user.password == info["password"]:
        access_token = create_access_token(identity=user.id)
        return jsonify({"valid": "true", "access_token": access_token})
    else:
        return jsonify({"valid":"false", "access_token": ""}), 401

@auth.route('/create_user', methods=['POST'])   
def create_user():
    info = request.json
    user = User.query.filter_by(email=info["email"]).first()
    if not user:
        new_user = User(email=info["email"], firstName=info["firstName"], password=info["password1"])
        db.session.add(new_user)
        db.session.commit()
        
    return jsonify({"status":"sucessful"}), 200

@auth.route('/confirm_token', methods=['POST']) 
def confirm_token():
    token = request.json["access_token"]
    if token:
        try:
            # Проверяем токен
            verify_jwt_in_request()
            return jsonify({'status': 'correct'}), 200
        
        except Exception as e:
            return jsonify({'status': str(e)}), 401

    return jsonify({'status': 'Missing token'}), 400

@auth.route('/get_rights', methods=['POST']) 
def get_rights():
    token = request.json["access_token"]
    project_part_id = ["project_part_id"]
    #try:
    verify_jwt_in_request()
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    return jsonify({'permissions': user.projectsAuthInfo}), 200
    
    #except Exception as e:
    #    return jsonify({'status': str(e)}), 401
    
    
@auth.route('/', methods=['GET']) 
def home_page():

    return jsonify({'1': 1}), 200  
