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
        "__table_args__": {},
    }

    tbl_class = type(
        "{class_name}".format(class_name=tbl_name.upper()),
        (OrmBase,),
        objects
    )

    return tbl_class


def get_table_model(conn: sa.engine.Engine, table: str, db_name=None):
    meta = sa.MetaData()

    # TODO: (bug) 未知数据库是否有区分大小写的表名
    guess_tables = [table, table.lower(), table.upper()]
    guess_tables = list(set(guess_tables))

    for guess_table in guess_tables:
        try:
            meta.reflect(bind=conn, schema=db_name, only=[guess_table])

            if db_name:
                key = "{schema}.{table}".format(schema=db_name, table=guess_table)
            else:
                key = guess_table

            return meta.tables[key]

        except sa.exc.InvalidRequestError:
            pass

    return None
