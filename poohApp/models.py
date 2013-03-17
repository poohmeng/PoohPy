# Create your models here.
#-*- coding: UTF-8 -*-
from mongoengine import *
from PoohPy.settings import DBNAME
from mongoengine.django.auth import User

from django.db import models
from django.contrib import admin
from mongoengine import Document, fields, DO_NOTHING, CASCADE
from django.core.urlresolvers import reverse
from djangotoolbox.fields import ListField, EmbeddedModelField


connect('test')

# class Post(Document):
#     title = StringField(max_length=120, required=True)
#     content = StringField(max_length=500, required=True)
#     last_update = DateTimeField(required=True)
#
class Users(User):
    GENDER_CHOICE = ((u'男', u'男'), (u'女', u'女'))
    gender = StringField(choices=GENDER_CHOICE, max_length=2)


# class Update(models.Model):
#     timestamp = models.DateTimeField(auto_now_add=True)
#     text = models.TextField()
#
#     class Meta:
#         ordering = ['-id']
#
#     def __unicode__(self):
#         return "[%s] %s" % (
#             self.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
#             self.text
#         )
#
# admin.site.register(Update)

class Post(Document):

    title = fields.StringField(max_length=255)
    created_at = fields.DateTimeField()
    body = fields.StringField()
    # tags = ListField(StringField(max_length=30))
    # comments = ListField(EmbeddedDocumentField(Comment))


# class TextPost(Post):
#     content = StringField()
#
# class ImagePost(Post):
#     image_path = StringField()
#
# class LinkPost(Post):
#     link_url = StringField()


class Comment(EmbeddedDocument):
    content = StringField()
    name = StringField(max_length=120)
    created_at = fields.DateTimeField()



