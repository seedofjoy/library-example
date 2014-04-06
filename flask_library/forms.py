# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, EqualTo, Length
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
from wtforms_alchemy import model_form_factory
from flask_library import db
from flask_library.models import Book, Author, User
ModelForm = model_form_factory(Form)


class AuthorForm(ModelForm):
    class Meta:
        model = Author
        strip_string_fields = True
        exclude = ('search_name',)

AuthorForm.books = QuerySelectMultipleField(
    u'Книги автора',
    query_factory=lambda: db.session.query(Book),
    get_label='title')


class BookForm(ModelForm):
    class Meta:
        model = Book
        strip_string_fields = True
        exclude = ('search_title',)

BookForm.authors = QuerySelectMultipleField(
    u'Авторы',
    query_factory=lambda: db.session.query(Author),
    get_label='name')


class SearchForm(Form):
    search = StringField(u'Поиск', validators=[InputRequired()])


class LoginForm(Form):
    email = EmailField(u'E-mail', validators=[InputRequired()])
    password = PasswordField(u'Пароль', validators=[InputRequired()])
    remember = BooleanField(u'Запомнить меня')

    def validate(self):
        success = super(LoginForm, self).validate()
        if not success:
            return False

        user = User.query.filter_by(email=self.email.data).first()
        if user is None:
            self.email.errors.append(
                u'Пользователь с таким адресом электронной почты не найден.')
            return False

        if not user.check_password(self.password.data):
            self.password.errors.append(u'Вы ввели неправильный пароль.')
            return False

        self.user = user
        return True


class RegistrationForm(Form):
    email = EmailField(u'E-mail', validators=[InputRequired(),
                                              Length(max=120)])
    password = PasswordField(u'Пароль', validators=[InputRequired()])
    password2 = PasswordField(u'Пароль еще раз', validators=[
        InputRequired(),
        EqualTo('password', message=u'Пароли должны совпадать!')]
    )

    def validate(self):
        success = super(RegistrationForm, self).validate()
        if not success:
            return False

        if User.query.filter_by(email=self.email.data).count() > 0:
            self.email.errors.append(u'Пользователь с таким адресом '
                                     u'электронной почты уже существует.')
            return False

        return True
