import datetime

import config

from flask_bcrypt import generate_password_hash
from peewee import *
from flask_login import UserMixin

DATABASE = SqliteDatabase('tasks.sqlite')


class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()

    class Meta:
        database = DATABASE

    @classmethod
    def create_user(cls, username, email, password, **kwargs):
        email = email.lower()
        try:
            cls.select().where(
                (cls.email == email) | (cls.username ** username)
            ).get()
        except cls.DoesNotExist:
            user = cls(username=username, email=email)
            user.password = generate_password_hash(password)
            user.save()
            return user
        else:
            raise Exception("User with that email or username already exists")


class Todo(Model):
    name = CharField(unique=True)
    completed = BooleanField(default=False)
    edited = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.datetime.now)
    user = ForeignKeyField(
        rel_model=User
    )

    class Meta:
        database = DATABASE


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Todo], safe=True)
    DATABASE.close()
    print('initialize')
