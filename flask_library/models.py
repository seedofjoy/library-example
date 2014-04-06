# -*- coding: utf-8 -*-
from werkzeug.security import check_password_hash, generate_password_hash
from flask_library import app, db
from flask.ext.login import UserMixin


def lower(field):
    return lambda context: context.current_parameters[field].lower()


authors = db.Table(
    'authors',
    db.Column('book_id', db.Integer, db.ForeignKey('book.id')),
    db.Column('author_id', db.Integer, db.ForeignKey('author.id'))
)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50),
                      unique=True,
                      nullable=False,
                      info={'label': u'Название'})
    search_title = db.Column(db.String(50),
                             default=lower('title'),
                             onupdate=lower('title'))
    authors = db.relationship('Author', secondary=authors,
        backref=db.backref('books', lazy='dynamic'))

    def __init__(self, title=None):
        self.title = title

    def __repr__(self):
        return u'<Book %r>' % (self.title)

    def __unicode__(self):
        return u'%s' % (self.title)


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),
                     unique=True,
                     nullable=False,
                     info={'label': u'Имя'})
    search_name = db.Column(db.String(50),
                            default=lower('name'),
                            onupdate=lower('name'))

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return u'<Author %r>' % (self.name)

    def __unicode__(self):
        return u'%s' % (self.name)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column('email', db.String(120), unique=True, index=True)
    password = db.Column('password', db.String(64))

    def __init__(self, email=None, password=None):
        self.email = email
        if password is not None:
            self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return u'<User %r>' % (self.email)

    def __unicode__(self):
        return u'%s' % (self.email)
