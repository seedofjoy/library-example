# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for, request, g
from flask.ext.login import (
    login_required, login_user, logout_user, current_user)
from flask_library import app, db, login_manager
from flask_library.models import Book, Author, User
from flask_library.forms import (
    BookForm, AuthorForm, SearchForm, LoginForm, RegistrationForm)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.before_request
def before_request():
    g.user = current_user


@app.route('/')
def index():
    return redirect(url_for('book_list'), code=301)


@app.route('/book')
def book_list():
    books = Book.query.all()
    return render_template('book_list.html', books=books)


@app.route('/author')
def author_list():
    authors = Author.query.all()
    return render_template('author_list.html', authors=authors)


@app.route('/book/<int:book_id>', methods=['GET', 'POST'])
@login_required
def book_edit(book_id):
    book = Book.query.get_or_404(book_id)
    form = BookForm(obj=book)

    if form.validate_on_submit():
        form.populate_obj(book)
        db.session.commit()
        flash(u'Книга "{0}" сохранена.'.format(book.title), category='success')
        return redirect(url_for('book_list'))
    return render_template(
        'edit.html',
        form=form,
        delete_url=url_for('book_delete', book_id=book_id)
    )


@app.route('/author/<int:author_id>', methods=['GET', 'POST'])
@login_required
def author_edit(author_id):
    author = Author.query.get_or_404(author_id)
    form = AuthorForm(obj=author)

    if form.validate_on_submit():
        form.populate_obj(author)
        db.session.commit()
        flash(u'Автор "{0}" сохранен.'.format(author.name), category='success')
        return redirect(url_for('author_list'))
    return render_template(
        'edit.html',
        form=form,
        delete_url=url_for('author_delete', author_id=author_id)
    )


@app.route('/book/<int:book_id>/delete', methods=['GET', 'POST'])
@login_required
def book_delete(book_id):
    book = Book.query.get_or_404(book_id)
    redirect_url = url_for('book_list')
    if request.method == 'POST':
        db.session.delete(book)
        db.session.commit()
        flash(u'Книга "{0}" удалена.'.format(book.title), category='warning')
        return redirect(redirect_url)
    return render_template(
        'delete_confirm.html',
        obj=book,
        redirect_to=redirect_url
    )


@app.route('/author/<int:author_id>/delete', methods=['GET', 'POST'])
@login_required
def author_delete(author_id):
    author = Author.query.get_or_404(author_id)
    redirect_url = url_for('author_list')
    if request.method == 'POST':
        db.session.delete(author)
        db.session.commit()
        flash(u'Автор "{0}" удален.'.format(author.name), category='warning')
        return redirect(redirect_url)
    return render_template(
        'delete_confirm.html',
        obj=author,
        redirect_to=redirect_url
    )


@app.route('/book/add', methods=['GET', 'POST'])
@login_required
def book_add():
    form = BookForm()
    if form.validate_on_submit():
        book = Book()
        form.populate_obj(book)
        db.session.add(book)
        db.session.commit()
        flash(u'Книга "{0}" добавлена.'.format(book.title), category='success')
        return redirect(url_for('book_list'))
    return render_template('edit.html', form=form)


@app.route('/author/add', methods=['GET', 'POST'])
@login_required
def author_add():
    form = AuthorForm()
    if form.validate_on_submit():
        author = Author()
        form.populate_obj(author)
        db.session.add(author)
        db.session.commit()
        flash(u'Автор "{0}" добавлен.'.format(author.name), category='success')
        return redirect(url_for('author_list'))
    return render_template('edit.html', form=form)


@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if not form.validate_on_submit():
        return render_template('search_results.html')

    query = form.search.data
    escaped_query = (query.replace('/', '//')
                          .replace('%', '/%')
                          .replace('_', '/_'))
    safe_query = u'%{}%'.format(escaped_query)
    books_results = Book.query.filter(
        Book.search_title.ilike(safe_query, escape='/')).all()
    authors_results = Author.query.filter(
        Author.search_name.ilike(safe_query, escape='/')).all()
    return render_template(
        'search_results.html',
        query=query,
        books=books_results,
        authors=authors_results,
        form=form
    )


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user.is_authenticated():
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = form.user
        remember = form.remember.data
        login_user(user, remember=remember)
        flash(u'Добро пожаловать, {0}'.format(user), category='info')
        return redirect(request.args.get('next') or url_for('index'))
    return render_template('login.html', form=form)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if g.user.is_authenticated():
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(request.args.get('next') or url_for('index'))
    return render_template('registration.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
