import datetime
from mongoengine import Document, StringField, DateTimeField, QuerySetManager


class User(Document):
    email = StringField(required=True)
    password = StringField(max_length=200, required=True)
    creation_date = DateTimeField(default=datetime.datetime.utcnow)
    objects = QuerySetManager()
