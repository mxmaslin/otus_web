import datetime

from flask_login import UserMixin

from app import db, login

from werkzeug.security import generate_password_hash, check_password_hash


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


tag_identifier = db.Table(
    'tag_identifier',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'))
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(40), nullable=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'{self.name}'


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    title = db.Column(db.String(120), nullable=False)
    body = db.Column(db.Text(120), nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.now())
    user = db.relationship('User', foreign_keys='Post.user_id')
    tags = db.relationship('Tag', secondary=tag_identifier)

    def __repr__(self):
        return f'{self.title}'


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'{self.name}'
