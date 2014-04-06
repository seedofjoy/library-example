# -*- coding: utf-8 -*-
from werkzeug.security import generate_password_hash
from fixture import DataSet, SQLAlchemyFixture
from fixture.style import NamedDataStyle
from flask_library import db, models
 
 
def install(app, *args):
    dbfixture = SQLAlchemyFixture(env=models, style=NamedDataStyle(),
                                  engine=db.engine)
    data = dbfixture.data(*args)
    data.setup()
    dbfixture.dispose()
 
 
class BookData(DataSet):

    class ulysses:
        title = u'Улисс'

    class jusforfun:
        title = u'Just for Fun'

    class hackers:
        title = u'Hackers: Heroes of the Computer Revolution'

    class nadya:
        title = u'Надя'

    class stranger:
        title = u'Посторонний'

    class wood:
        title = u'Норвежский лес'

    class clockwork:
        title = u'Хроники Заводной Птицы'


class AuthorData(DataSet):

    class joyce:
        name = u'Джеймс Джойс'
        books = [BookData.ulysses]

    class torvalds:
        name = u'Linus Torvalds'
        books = [BookData.jusforfun]

    class diamond:
        name = u'David Diamond'
        books = [BookData.jusforfun]

    class levy:
        name = u'Steven Levy'
        books = [BookData.hackers]

    class breton:
        name = u'Андре Бретон'
        books = [BookData.nadya]

    class camus:
        name = u'Альбер Камю'
        books = [BookData.stranger]

    class murakami:
        name = u'Харуки Мураками'
        books = [
            BookData.wood,
            BookData.clockwork,
        ]


class UserData(DataSet):

    class test:
        email = 'test@test.com'
        password = generate_password_hash('123')


all_data = (BookData, AuthorData, UserData,)
