import datetime
from mongoengine import Document, StringField, DateTimeField, QuerySetManager


class RequestLog(Document):
    user = StringField(required=True)
    request_body = StringField(required=True)
    request_headers = StringField(required=True)
    date = DateTimeField(default=datetime.datetime.utcnow)
    objects = QuerySetManager()
