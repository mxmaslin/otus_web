import os
import random

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from faker import Faker

from models import Link, User, Post, Tag, Model


def create_tag_or_user(amount, model, provider):
    instances = []
    for i, _ in enumerate(range(amount)):
        name = provider()
        instance = model(name=name)
        session.add(instance)
        instances.append(instance)
    session.commit()
    return instances


def create_posts(amount, post_users, post_tags):
    for i, _ in enumerate(range(amount)):
        user = post_users[random.randint(0, len(users) - 1)]
        title = fake.sentence()
        body = fake.text()
        tags = [post_tags[n] for n in range(random.randint(0, len(post_tags) - 1))]
        post = Post(user=user, title=title, body=body)
        post.tags.extend(tags)
    session.commit()


os.remove('db.sqlite')
engine = create_engine('sqlite:///db.sqlite')
Model.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

fake = Faker('ru_RU')

users_amount = 5
users = create_tag_or_user(users_amount, User, fake.name)

tags_amount = 10
tags = create_tag_or_user(tags_amount, Tag, fake.word)

posts_amount = 10
create_posts(posts_amount, users, tags)

os.remove('db.sqlite')
engine = create_engine('sqlite:///db.sqlite')
Model.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

fake = Faker('ru_RU')

users_amount = 5
users = create_tag_or_user(users_amount, User, fake.name)

tags_amount = 10
tags = create_tag_or_user(tags_amount, Tag, fake.word)

posts_amount = 10
create_posts(posts_amount, users, tags)

