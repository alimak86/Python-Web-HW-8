from datetime import datetime

from mongoengine import EmbeddedDocument, Document
from mongoengine.fields import BooleanField, DateTimeField, EmbeddedDocumentField, ListField, StringField, ReferenceField

import json
from abc import ABC, abstractmethod
from collections import UserDict


class Author(Document):
    fullname = StringField()
    born_date = StringField()
    born_location = StringField()
    description = StringField()


class Authors(UserDict):

    def __init__(self):
        self.data = {}

    def append(self, author: Author):
        self.data[author.fullname] = author


class Quote(Document):
    tags = ListField()
    author = ReferenceField(Author)
    quote = StringField()


class Contact(Document):
    fullname = StringField()
    email = StringField()
    sent = BooleanField(default=False)
