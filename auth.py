from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.authenticate(username, password)
        if user:
            login_user(user)
            # Limpar setor anterior ao fazer login
            if 'setor' in session:
                session.pop('setor')
            return redirect('/selecionar-setor')
        else:
            flash('Usuario ou senha invalidos', 'error')
    
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    if session:
        session.clear()
    return redirect('/login')