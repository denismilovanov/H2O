'''
Some decorators
'''

# for raw_queries
from django.db import models
from django.db import connections, transaction
from functools import *
import psycopg2
import types

# for render_to
from django.shortcuts import render_to_response
from django.template import RequestContext

psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)


def raw_queries(dbs=[]):
    if (dbs == None):
        dbs = []

    if (len(dbs) == 0):
        dbs = ['default']

    def raw_queries_db(func):

        def select_table(db, query, *args, **kwargs):
            db.execute(query, kwargs)
            desc = db.description
            result = [
                dict(zip([col[0] for col in desc], row))
                for row in db.fetchall()
            ]
            return result

        def select_record(db, query, *args, **kwargs):
            db.execute(query, kwargs)
            desc = db.description
            result = [
                dict(zip([col[0] for col in desc], row))
                for row in db.fetchmany(1)
            ]
            try:
                return result[0]
            except:
                return None

        def select_field(db, query, *args, **kwargs):
            db.execute(query, kwargs)
            row = db.fetchmany(1)
            try:
                result = row[0][0]
                return result
            except:
                return None

        def query(db, query, *args, **kwargs):
            return db.execute(query, kwargs)

        def t(db):
            return transaction.atomic(db.name)

        def inner(*args, **kwargs):
            for db in dbs:
                if db == 'matches':
                    user_id = args[0]
                    # there is only 1 database now, with number 0
                    db = 'matches' + str(user_id % 1)
                    name = 'matches'
                else:
                    name = db

                cursor = connections[db].cursor()
                cursor.select_table = types.MethodType(select_table, cursor)
                cursor.select_record = types.MethodType(select_record, cursor)
                cursor.select_field = types.MethodType(select_field, cursor)
                cursor.t = types.MethodType(t, cursor)
                cursor.query = types.MethodType(query, cursor)
                kwargs[name if name != 'default' else 'db'] = cursor
            return func(*args, **kwargs)
        return inner

    return raw_queries_db



