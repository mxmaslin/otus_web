from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///orm.sqlite', echo=False)

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String)
    password = Column(String)

    # note = Column(String, nullable=True)

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __str__(self):
        return f'{self.id}) {self.email}: {self.password}'


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    text = Column(String, nullable=True)
    # Связь 1 - много, связь внешний ключ
    user_id = Column(Integer, ForeignKey('users.id'))

    def __init__(self, name, text, user_id):
        self.name = name
        self.text = text
        self.user_id = user_id


# Создание таблицы
Base.metadata.create_all(engine)

if __name__ == '__main__':
    # Заполняем таблицы
    Session = sessionmaker(bind=engine)

    # create a Session
    session = Session()

    # Регионы
    session.add_all([User('text@test.com', 'pass123')])

    first_user = session.query(User).first()

    session.add(Post('Тема', 'Текст', first_user.id))

    session.commit()

    print(session.query(User).all())
    print(session.query(Post).all())
