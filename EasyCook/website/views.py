from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from .models import User
from . import db
from os import path

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html", user=current_user)

@views.route('/perfil')
@login_required
def perfil():
    return render_template("perfil.html", user=current_user, path=path)

@views.route('/editar_perfil', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        imagem = request.files['imagem']
        nome_arquivo = secure_filename(imagem.filename)

        if imagem.filename == "":
            pass
        elif nome_arquivo.split('.', 1)[1].lower() != 'jpg':
            flash('Formato de arquivo nao aceito', category='error')
        else:
            imagem.save(path.join('website/static/imagens_perfil', current_user.username + ".jpg"))

        user_email = User.query.filter_by(email=email).first()
        if user_email and user_email != current_user:
            flash('Email ja cadastrado', category='error')
        elif len(email) < 4 or len(email) > 150:
            flash('Email deve ter entre 4 e 150 caracteres', category='error')
        elif len(nome) < 2 or len(nome) > 150:
            flash('Nome deve ter entre 2 e 150 caracteres', category='error')
        else:
            user = User.query.filter_by(username=current_user.username).first()
            user.nome = nome
            user.email = email
            db.session.commit()
            flash('Informações atualizadas', category='success')
            return redirect(url_for('views.perfil'))
    return render_template("editar_perfil.html", user=current_user)

@views.route('/mudar_senha', methods=['GET', 'POST'])
@login_required
def mudar_senha():
    if request.method == 'POST':
        senha1 = request.form.get('senha1')
        senha2 = request.form.get('senha2')

        user = User.query.filter_by(username=current_user.username).first()
        if check_password_hash(user.senha, senha1):
            flash('Senha igual a senha atual', category='error')
        elif len(senha1) < 7 or len(senha1) > 150:
            flash('Senha deve ter entre 7 e 150 caracteres', category='error')
        elif senha1 != senha2:
            flash('Senhas nao coincidem', category='error')
        else:
            user.senha = generate_password_hash(senha1, method='sha256')
            db.session.commit()
            flash('Senha atualizada', category='success')
            return redirect(url_for('views.perfil'))
    return render_template("mudar_senha.html", user=current_user)