from datetime import *
from peewee import *
import os
from flask_bcrypt import generate_password_hash

DATABASE_proxy = Proxy()

if 'HEROKU' in os.environ:
    import urllib.parse, psycopg2

    urllib.parse.uses_netloc.append('postgres')
    url = urllib.parse.urlparse(os.environ["DATABASE_URL"])
    DATABASE = PostgresqlDatabase(database=url.path[1:], user=url.username, password=url.password, host=url.hostname,
                                  port=url.port)
    DATABASE_proxy.initialize(DATABASE)
else:
    DATABASE = SqliteDatabase('gradgoggles.db')
    DATABASE_proxy.initialize(DATABASE)


class User(Model):
    name = CharField(max_length=30, default=None, null=True)
    email = CharField(unique=True)
    password = CharField(max_length=150)
    joined_at = DateTimeField(default=datetime.now)
    isVerified = BooleanField(default=None, null=True)
    is2020 = BooleanField(default=None, null=True)
    isfeatured = IntegerField(default=0)

    quote = TextField(default=None, null=True)
    photo = CharField(max_length=200, default=None, null=True)
    gr = CharField(max_length=50, default=None, null=True)
    dob = DateTimeField(default=None, null=True)
    dept = CharField(default=None, null=True)

    @classmethod
    def create_user(cls, email, password, name, photo=None, gr=None, dept=None, dob=None, quote=None, isVerified=False,
                    is2020=False, isfeatured=0):
        try:
            with DATABASE.transaction():
                user = cls.create(
                    email=email,
                    password=generate_password_hash(password),
                    name=name,
                    gr=gr,
                    dept=dept,
                    dob=dob,
                    quote=quote,
                    photo=photo,
                    isVerified=isVerified,
                    is2020=is2020,
                    isfeatured=isfeatured
                )
                return user
        except IntegrityError:
            raise ValueError("User already exists")

    @classmethod
    def delete_user(cls, email):
        try:
            user_created = cls.get(cls.email == email)
            user_created.delete_instance()
        except:
            raise InternalError

    class Meta:
        database = DATABASE_proxy
        order_by = ('-joined_at',)


class Scrap(Model):
    posted_by = ForeignKeyField(model=User, related_name='posted_by')
    posted_to = ForeignKeyField(model=User, related_name='posted_for')
    content = TextField()
    timestamp = DateTimeField(default=datetime.now)
    visibility = BooleanField(default=False)

    class Meta:
        database = DATABASE_proxy
        order_by = ('-joined_at',)


def initialize():
    DATABASE_proxy.connection()
    DATABASE_proxy.create_tables([User, Scrap])
    DATABASE_proxy.close()
