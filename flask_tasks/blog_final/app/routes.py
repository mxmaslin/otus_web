from app import app
import os
import sqlalchemy

from passlib.hash import sha256_crypt
from flask import Flask, render_template, flash, request, redirect, url_for,\
    session
from flask_login import LoginManager, login_user
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .forms import RegistrationForm, LoginForm
from .models import Link, User, Post, Tag, session as db_session


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register/', methods=["GET", "POST"])
def register():
    form = RegistrationForm(request.form)

    if request.method == "POST" and form.validate():
        username = form.username.data
        password = sha256_crypt.hash((str(form.password.data)))
        user = User(name=username, password=password)
        db_session.add(user)
        db_session.commit()
        session['logged_in'] = True
        session['username'] = username
        return redirect(url_for('index'))

    return render_template('register.html', form=form)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db_session.query(
            User
        ).filter(User.name == form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неправильное имя пользователя или пароль')
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        return redirect(next_page or url_for('index'))
    return render_template('login.html', form=form)
