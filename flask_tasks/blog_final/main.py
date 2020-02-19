import os

import sqlalchemy

from passlib.hash import sha256_crypt
from flask import Flask, render_template, flash, request, redirect, url_for,\
    session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from forms import RegistrationForm
from models import Link, User, Post, Tag, session as db_session

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


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
        # flash('Спасибо за регистрацию')
        session['logged_in'] = True
        session['username'] = username
        return redirect(url_for('index'))

    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run()
