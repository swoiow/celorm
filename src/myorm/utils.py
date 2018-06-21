#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os
import pickle
import sys
import traceback
from contextlib import contextmanager
from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import Session

__all_ = ["db_write", "db_read", "OrmBase", "dynamic_table"]
cPickle = pickle


@contextmanager
def db_write(engine=None):
    """Provide a transactional scope around a series of operations."""

    engine = engine or os.environ.get("DATABASE_URI")
    session = Session(bind=engine)

    try:
        yield session
        session.commit()

    except Exception as e:
        session.rollback()
        traceback.print_exc()
        f_locals = sys.exc_info()[2].tb_next.tb_frame.f_locals

        _v = {k: v for k, v in f_locals.items() if isinstance(v, (str, bytes, dict, list, tuple))}
        _f = "session_{}.dmp".format(datetime.now().strftime("%Y%m%d%H%M%S_%f"))
        _p = os.path.join(os.getcwd(), _f)
        with open(_p, "wb") as wf:
            cPickle.dump(obj=_v, file=wf)
            print("Error and export dump in => {}".format(_p))

    finally:
        session.close()


@contextmanager
def db_read(engine=None):
    engine = engine or os.environ.get("DATABASE_URI")
    session = Session(bind=engine)

    try:
        yield session
    finally:
        session.close()


OrmBase = declarative_base()


def dynamic_table(cls_name, model, table_name=None):
    """ http://windrocblog.sinaapp.com/?p=1554
        http://docs.sqlalchemy.org/en/latest/orm/extensions/declarative/mixins.html

    record_table_mapper = {}
    class PotentialModel(OrmBase):
        __tablename__ = "test-table"
        id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
        name = sa.Column(sa.String(1000))

    a = dynamic_table("PotentialModel", PotentialModel, "PotentialModel")
    record_table_mapper["dyt_A"] = a

    engine = sa.create_engine("sqlite:///database.db")
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

    dict_ = table_name and {'__tablename__': table_name} or dict()

    table_object = type(
        'DYT_{class_name}'.format(class_name=cls_name),
        (model, OrmBase),
        dict_
    )

    return table_object
