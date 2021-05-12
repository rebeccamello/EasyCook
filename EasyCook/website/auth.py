from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        senha = request.form.get('senha')

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.senha, senha):
                flash('Logado com sucesso!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Senha incorreta, tente novamente', category='error')
        else:
            flash('Username não existe', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha1 = request.form.get('senha1')
        senha2 = request.form.get('senha2')

        user_username = User.query.filter_by(username=username).first()
        user_email = User.query.filter_by(email=email).first()

        if user_username:
            flash('Username já existente', category='error')
        elif user_email:
            flash('Email já cadastrado', category='error')
        elif len(username) < 3 or len(username) > 30:
            flash('Username deve ter entre 3 e 30 caracteres', category='error')
        elif len(email) < 4 or len(email) > 150:
            flash('Email deve ter entre 4 e 150 caracteres', category='error')
        elif len(nome) < 2 or len(nome) > 150:
            flash('Nome deve ter entre 2 e 150 caracteres', category='error')
        elif len(senha1) < 7 or len(senha1) > 150:
            flash('Senha deve ter entre 7 e 150 caracteres', category='error')
        elif senha1 != senha2:
            flash('Senhas nao coincidem', category='error')
        else:
            new_user = User(username=username, nome=nome, email=email, senha=generate_password_hash(senha1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Conta criada!', category='success')
            return redirect(url_for('views.home'))


    return render_template("sing_up.html", user=current_user)