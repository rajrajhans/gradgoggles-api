from datetime import *
from peewee import *
import os

DATABASE_proxy = Proxy()

if 'HEROKU' in os.environ:
    import urllib.parse

    urllib.parse.uses_netloc.append('postgres')
    url = urllib.parse.urlparse(os.environ["DATABASE_URL"])
    DATABASE = PostgresqlDatabase(database=url.path[1:], user=url.username, password=url.password, host=url.hostname,
                                  port=url.port)
    DATABASE_proxy.initialize(DATABASE)
else:
    DATABASE = SqliteDatabase('gradgoggles.db')
    DATABASE_proxy.initialize(DATABASE)


class User(Model):
    name = CharField(max_length=30)
    email = CharField(unique=True)
    password = CharField(max_length=150)
    joined_at = DateTimeField(default=datetime.now)

    quote = TextField()
    photo = CharField(max_length=200)
    gr = CharField(max_length=50)
    dob = DateTimeField()
    dept = CharField()

    class Meta:
        database = DATABASE_proxy
        order_by = ('-joined_at',)


class Scrap(Model):
    posted_by = ForeignKeyField(model=User,related_name='posted_by')
    posted_to = ForeignKeyField(model=User,related_name='posted_for')
    content = TextField()
    timestamp = DateTimeField(default=datetime.now)
    visibility = BooleanField(default=True)

    class Meta:
        database = DATABASE_proxy
        order_by = ('-joined_at',)


def initialize():
    DATABASE_proxy.connection()
    DATABASE_proxy.create_tables([User])
    DATABASE_proxy.close()
