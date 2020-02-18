from models import Model, Tag, Post, User
from populate_db import create_tag_or_user, fake, session


user = create_tag_or_user(1, User, fake.name)[0]
tags = [create_tag_or_user(1, Tag, fake.word)[0] for _ in range(2)]
post = Post(user=user, title=fake.sentence(), body=fake.text())
post.tags.extend(tags)
session.add(user)
session.add(tags[0])
session.add(tags[1])
session.add(post)
session.commit()

posts = session.query(
    Post
).join(User).filter(
    User.name == user.name
).filter(
    Post.tags.any(Tag.id.in_([tag.id for tag in tags]))
).all()
print(posts)
