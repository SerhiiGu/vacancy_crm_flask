from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from datetime import datetime
from al_db import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    email = Column(String(127), unique=True)
    login = Column(String(50), unique=True)
    password = Column(String(127), nullable=False)

    def __init__(self, name, email, login, password):
        self.name = name
        self.email = email
        self.login = login
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.name


class EmailCredentials(Base):
    __tablename__ = 'email_creds'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    email = Column(String(127), unique=True, nullable=False)
    login = Column(String(127), nullable=False)
    password = Column(String(127), nullable=False)
    pop_server = Column(String(127), nullable=False)
    smtp_server = Column(String(127), nullable=False)

    def __init__(self, login, password):
        self.login = login
        self.password = password

    def __repr__(self):
        return '<EmailCredentials %r>' % self.email


class Vacancy(Base):
    __tablename__ = 'vacancy'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    creation_date = Column(DateTime, default=datetime.utcnow)
    company = Column(String(127), nullable=False)
    position_name = Column(String(127), nullable=False)
    description = Column(String(255), nullable=False)
    comment = Column(String(255), nullable=False)
    contact_ids = Column(String(127), nullable=False)
    status = Column(Integer, nullable=False)

    def __init__(self, position_name, company, description, contact_ids, comment, status, user_id):
        self.position_name = position_name
        self.company = company
        self.description = description
        self.contact_ids = contact_ids
        self.comment = comment
        self.status = status
        self.user_id = user_id

    def __repr__(self):
        return '<Vacancy %r>' % [self.position_name, self.company]


class Event(Base):
    __tablename__ = 'event'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    vacancy_id = Column(Integer, ForeignKey('vacancy.id'))
    description = Column(String(255), nullable=False)
    event_date = Column(DateTime, default=datetime.utcnow)
    title = Column(String(50), nullable=False)
    due_to_date = Column(String(50), nullable=False)
    status = Column(Integer, nullable=False)

    def __init__(self, vacancy_id, title, description, due_to_date, status):
        self.vacancy_id = vacancy_id
        self.title = title
        self.description = description
        self.due_to_date = due_to_date
        self.status = status

    def __repr__(self):
        return '<Event %r>' % [self.title, self.description]


class Template(Base):
    __tablename__ = 'template'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))

    def __init__(self, name, content):
        self.name = name
        self.content = content

    def __repr__(self):
        return '<Template %r>' % self.name


class Document(Base):
    __tablename__ = 'document'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    description = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))

    def __init__(self, name, content):
        self.name = name
        self.content = content

    def __repr__(self):
        return '<Document %r>' % self.name
