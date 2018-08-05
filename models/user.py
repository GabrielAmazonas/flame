import datetime
from mongoengine import Document, StringField, QuerySetManager


class User(Document):
    email = StringField(required=True)
    password = StringField(max_length=200, required=True)
    objects = QuerySetManager()
