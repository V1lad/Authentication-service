from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from .models import User
from . import db
import bcrypt
from flask_jwt_extended import create_access_token, verify_jwt_in_request

auth = Blueprint('auth', __name__)

# Отвечает за вход в аккаунт
@auth.route('', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        print(user)
        if user:
            if user.password == password:
                flash('Вы успешно вошли в аккаунт', category='success')
                return redirect(url_for('views.home'))
            else:
                flash('Неверный пароль', category='error')
        else:
            flash('Аккаунта с такой почтой не существует', category='error')
            
    return render_template("login.html")

# Отвечает за выход из аккаунта
@auth.route('/logout')
def logout():
    return redirect(url_for('auth.login'))

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

def get_user_rights():
    pass

def terminate_token():
    pass