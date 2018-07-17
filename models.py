import datetime
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          BadSignature, SignatureExpired)
from peewee import *
from argon2 import PasswordHasher
from config import SECRET_KEY
from flask_login import UserMixin

DATABASE = SqliteDatabase('tasks.sqlite')
HASHER = PasswordHasher()


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
            user.password = user.set_password(password)
            user.save()
            return user
        else:
            raise Exception("User with that email or username already exists")

    @staticmethod
    def verify_auth_token(token):
        serializer = Serializer(SECRET_KEY)
        try:
            data = serializer.loads(token)
        except (SignatureExpired, BadSignature):
            print('None')
            return None
        else:
            user = User.get(User.id == data['id'])
            return user

    @staticmethod
    def set_password(password):
        return HASHER.hash(password)

    def verify_password(self, password):
        return HASHER.verify(self.password, password)

    def generate_auth_token(self):
        serializer = Serializer(SECRET_KEY)
        return serializer.dumps({'id': self.id})


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
