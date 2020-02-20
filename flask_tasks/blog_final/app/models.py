import datetime

from sqlalchemy import create_engine, Column, Integer, DateTime, String, \
    Text, ForeignKey, Table
from sqlalchemy.orm import sessionmaker, backref, relationship
from sqlalchemy.ext.declarative import declarative_base

from flask_login import UserMixin, LoginManager

from app import app

login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


Model = declarative_base(name='Model')


class Link(Model):
    __tablename__ = 'link'
    post_id = Column(
        Integer,
        ForeignKey('post.id'),
        primary_key=True
    )
    tag_id = Column(
        Integer,
        ForeignKey('tag.id'),
        primary_key=True
    )


class User(UserMixin, Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    password = Column(String(40), nullable=False)

    def __repr__(self):
        return f'{self.name}'


class Post(Model):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id))
    title = Column(String(120), unique=True, nullable=False)
    body = Column(Text(120), nullable=False)
    created = Column(DateTime, default=datetime.datetime.now())
    user = relationship('User', foreign_keys='Post.user_id')
    tags = relationship('Tag', secondary='link')

    def __repr__(self):
        return f'{self.title}'


class Tag(Model):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    posts = relationship('Post', secondary='link')

    def __repr__(self):
        return f'{self.name}'


engine = create_engine('sqlite:///db.sqlite')
Model.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


# vasya = User(name='Вася')
# petya = User(name='Петя')
# lena = User(name='Лена')
# session.add(vasya)
# session.add(petya)
# session.add(lena)
#
# tag_1 = Tag(name='Интересно')
# tag_2 = Tag(name='Очень интересно')
# tag_3 = Tag(name='Не интересно')
# session.add(tag_1)
# session.add(tag_2)
#
#
# post_1 = Post(user=vasya, title='Заголовок Вася 1', body='Содержание')
# post_1.tags.append(tag_1)
# session.add(post_1)
# post_2 = Post(user=petya, title='Заголовок Петя 1', body='Содержание')
# session.add(post_2)
#
# post_3 = Post(user=lena, title='Заголовок Лена 1', body='Содержание')
# post_3.tags.append(tag_3)
# session.add(post_3)
# post_4 = Post(user=lena, title='Заголовок Лена 2', body='Содержание')
# post_4.tags.append(tag_1, tag_2)
# session.add(post_4)
# post_5 = Post(user=lena, title='Заголовок Лена 3', body='Содержание')
# post_5.tags.append(tag_1, tag_2)
# session.add(post_5)
# session.commit()
#
# interesting_tags = session.query(Tag).filter(Tag.name.in_(['Интересно', 'Очень интересно'])).all()
#
# posts = session.query(
#     Post
# ).join(User).filter(
#     User.name == 'Лена'
# ).filter(
#     Post.tags.any(Tag.id.in_([tag.id for tag in interesting_tags]))
# ).all()
# print(posts)
