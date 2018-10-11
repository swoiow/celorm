#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
doc: http://docs.sqlalchemy.org/en/latest/orm/contextual.html
"""

from __future__ import absolute_import

import datetime as dt
import os
import sys
import traceback
from contextlib import contextmanager

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import Session


try:
    import pickle
except ImportError:
    import cPickle as pickle

__all_ = ["db_write", "db_read", "dynamic_table", "OrmBase", ]


@contextmanager
def db_write(engine=None):
    """ Provide a transactional scope around a series of operations. """

    engine = engine or os.environ.get("DATABASE_URI")
    session = Session(bind=engine)
    # Session = scoped_session(
    #     sessionmaker(bind=engine, autocommit=False, autoflush=False)
    # )

    try:
        yield session
        session.commit()

    except Exception as e:
        session.rollback()
        catch_exception(type_="w")

    finally:
        session.close()


@contextmanager
def db_read(engine=None):
    engine = engine or os.environ.get("DATABASE_URI")
    session = Session(bind=engine)

    try:
        yield session

    except Exception as e:
        catch_exception(type_="r")

    finally:
        session.close()


def catch_exception(type_):
    type_ = type_.upper()
    fn = "orm{0}_{1}.dmp".format(type_, dt.datetime.now().strftime("%Y%m%d%H%M%S_%f"))

    f_locals = sys.exc_info()[2].tb_next.tb_frame.f_locals
    _v = {k: v for k, v in f_locals.items() if isinstance(v, (str, bytes, dict, list, tuple))}
    _v["__tb"] = traceback.format_exc()

    fp = os.path.join(os.getcwd(), fn)
    with open(fp, "wb") as wf:
        pickle.dump(obj=_v, file=wf)
        print("[{0}] Error and export dump in => {1}".format(type_, fp))


class MyORMBase(object):
    # query = Session.query_property()

    @staticmethod
    def row2dict(r):
        # TODO: getattr 可能存在bug, 没有读取字段为空时的默认值.

        if hasattr(r, "__table__"):
            return {c.name: getattr(r, c.name) for c in r.__table__.columns}
        else:
            return {c: getattr(r, c) for c in r._fields}

    def to_dict(self):
        return self.row2dict(self)

    def _init_more(self, **kwargs):
        for obj in (f for f in self.__class__.__dict__.keys() if not f.startswith("_")):
            if kwargs.get(obj):
                setattr(self, obj, kwargs[obj])

    def __repr__(self):
        return "<%s @%#x>" % (self.__class__.__name__, id(self))


OrmBase = declarative_base(cls=MyORMBase)


def dynamic_table(cls_name, model, table_name=None):
    """
        http://windrocblog.sinaapp.com/?p=1554
        http://docs.sqlalchemy.org/en/latest/orm/extensions/declarative/mixins.html

    record_table_mapper = {}
    
    # TODO: 如果类继承于 OrmBase， 则出现 sqlalchemy.exc.NoForeignKeysError 的问题
    class PotentialModel(object):
        __tablename__ = "test-table"
        id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
        name = sa.Column(sa.String(1000))

    a = dynamic_table("PotentialModel", PotentialModel, "PotentialModel")
    record_table_mapper["dyt_A"] = a

    engine = sa.create_engine("sqlite://")
    session = Session(bind=engine)

    OrmBase.metadata.create_all(engine)

    with db_write(engine) as db:
        b = a(name="abc123")
        db.add(b)
        c = a(name="qqq321")
        db.add(c)

    with db_read(engine) as db:
        q = db.query(a)
        print(q.all())
    """

    attrs = {}
    if table_name:
        attrs["__tablename__"] = table_name

    table_object = type(
        "DYT_{class_name}".format(class_name=cls_name),
        (model, OrmBase),
        attrs
    )

    return table_object
