import datetime
from mongoengine import Document, StringField, QuerySetManager


class RequestLog(Document):
    user = StringField(required=True)
    request_body = StringField(required=True)
    request_headers = StringField(required=True)
    objects = QuerySetManager()
