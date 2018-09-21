#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlalchemy as sa


def generate_sql_exec(table_name, item):
    columns = ", ".join(item.keys())
    placeholders = ", ".join(["%s"] * len(item))
    sql_exec = "INSERT INTO %s ( %s ) VALUES ( %s );" % (table_name, columns, placeholders)

    return sql_exec


def generate_table_class(tbl: sa.Table):
    def _repr_(self):
        return "<%s @%#x>" % (self.__tablename__.upper(), id(self))

    from .utils import OrmBase

    tbl_name = tbl.fullname
    objects = {
        "__table__": tbl,
        "__tablename__": tbl_name,
        "__repr__": _repr_,
    }

    tbl_class = type(
        "{class_name}".format(class_name=tbl_name.upper()),
        (OrmBase,),
        objects
    )

    return tbl_class


def get_table_model(conn: sa.engine.Engine, table: str, db_name=None):
    meta = sa.MetaData()
    meta.reflect(bind=conn, schema=db_name)

    guess_tables = set()
    guess_tables.add(table)
    guess_tables.add(table.lower())
    guess_tables.add(table.upper())

    if db_name:
        _ = ".".join([db_name, table])
        guess_tables.add(_)

        _ = ".".join([db_name, table.lower()])
        guess_tables.add(_)

        _ = ".".join([db_name, table.upper()])
        guess_tables.add(_)

    for guess_table in guess_tables:
        try:
            return meta.tables[guess_table]
        except KeyError:
            pass

    return None
