from app import app, db

from flask import render_template, flash, request, redirect, url_for,\
    session
from flask_login import current_user, login_user, logout_user, login_required

from .forms import RegistrationForm, LoginForm, PostForm
from .models import Link, User, Post, Tag


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(name=form.username.data, password=form.password.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Поздравляем, вы зарегистрированы!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('index.html')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неправильное имя пользователя или пароль')
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        return redirect(next_page or url_for('index'))
    return render_template('login.html', form=form)


@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/user/<username>/')
@login_required
def user(username):
    user = User.query.filter_by(name=username).first_or_404()
    posts = [
        {'author': user, 'title': 'Заголовок первого поста',
         'body': 'Контент первого поста', 'created': 'today', 'tags': []},
        {'author': user, 'title': 'Заголовок второго поста', 'body':
            'Контент второго поста',
         'created': 'today', 'tags': []}
    ]
    return render_template('user.html', user=user, posts=posts)


@app.route('/create/', methods=['GET', 'POST'])
@login_required
def create():
    form = PostForm()
    if form.validate_on_submit():
        # user = User.query.filter_by(name=current_user.name)
        # print(user)
        return redirect(url_for('user', username=current_user.name))
    return render_template('create-post.html', form=form)
