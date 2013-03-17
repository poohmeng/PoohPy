from django.shortcuts import render_to_response

__author__ = 'mengmeng'

from pymongo import Connection
from PoohPy.settings import  *


def connect_database():

    if DATABASE_USERNAME is None:
        host = 'mongodb://%s:%d' % (DATABASE_HOST, DATABASE_PORT)
    else:
        host = 'mongodb://%s:%s@%s:%d' % \
               (DATABASE_USERNAME, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_PORT)

    c = Connection(host)
    return c['poohApp_users']





