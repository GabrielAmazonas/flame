import datetime
from mongoengine import Document, StringField, QuerySetManager


class User(Document):
    email = StringField(required=True)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)
    password = StringField(max_length=200)
    objects = QuerySetManager()
