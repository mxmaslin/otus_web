from app import app, db

from flask import render_template, flash, request, redirect, url_for, session
from flask_login import current_user, login_user, logout_user, login_required

from .forms import RegistrationForm, LoginForm, PostForm
from .models import User, Post, Tag
from .filters import format_datetime

app.jinja_env.filters['formatdatetime'] = format_datetime


@app.route('/')
@app.route('/index/')
def index():
    posts = Post.query.order_by(Post.created.desc()).all()
    return render_template('index.html', posts=posts)


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
        return redirect(url_for('index'))
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
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/user/<username>/')
def user_posts(username):
    user = User.query.filter_by(name=username).first_or_404()
    posts = Post.query.filter_by(user=user).all()
    same_user = user.name == current_user.name
    return render_template(
        'user-posts.html',
        username=username,
        same_user=same_user,
        posts=posts
    )


@app.route('/create/', methods=['GET', 'POST'])
@login_required
def create():
    form = PostForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=current_user.name).first()
        title = form.title.data
        body = form.body.data
        tags = form.tags.data
        post = Post(title=title, body=body, user=user)
        for tag in tags:
            db.session.add(tag)
            post.tags.append(tag)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('user_posts', username=current_user.name))
    return render_template('create-post.html', form=form)


@app.route('/edit/<pk>/', methods=['GET', 'POST'])
@login_required
def edit(pk):
    post = Post.query.filter(Post.id == pk).first_or_404()
    if request.method == 'POST':
        form = PostForm(request.form, obj=post)
        if form.validate():
            form.populate_obj(post)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('detail', pk=post.id))
    else:
        form = PostForm(obj=post)
    return render_template('edit-post.html', post=post, form=form)


@app.route('/detail/<pk>/')
def detail(pk):
    post = Post.query.filter_by(id=pk).first()
    author = post.user.name
    same_author = author == current_user.name
    return render_template('post.html', post=post, author=author, same_author=same_author)


@app.route('/tag/<pk>/')
def tag(pk):
    posts = Post.query.join(Tag).filter(Post.tags.any(Tag.id == pk))
    print(posts)
    return render_template('tag.html', posts=posts)
