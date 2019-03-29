#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import threading
import time, random
from src.orm import SESSION, create_engine, db_read, db_write


class MyTestCase(unittest.TestCase):

    def test_sqlite(self):
        SESSION.configure(bind=create_engine("sqlite://"))
        self._test_case()

    def test_pgsql(self, thread=True, thread_num=10000):
        SESSION.configure(bind=create_engine("postgresql+psycopg2://postgres:admin@10.2.0.49:5432/postgres",
                                             connect_args={}))

        if thread:
            for i in range(thread_num):
                t = threading.Thread(target=self._test_case)
                t.setDaemon(True)
                t.start()

            t.join()

        else:
            self._test_case()

    def _test_case(self):
        ts = random.sample(range(1,10),1)[0]
        # self._test_create_table()
        self._test_insert_table()

        time.sleep(ts)
        t = self._get_pgsql_client_number()
        print(threading.activeCount(), threading.currentThread().getName(), ts, t)

        self._test_query_table()
        # self._test_drop_table()

    def _get_pgsql_client_number(self):
        with db_read() as db:
            rst = db.execute('SELECT count(*) FROM pg_stat_activity;')
            _ = rst.fetchall()
            return _[0]

    def _test_create_table(self):
        with db_write() as db:
            rst = db.execute("CREATE TABLE test_db (id INTEGER);")

    def _test_insert_table(self):
        with db_write() as db:
            rst = db.execute('INSERT INTO test_db VALUES (1);')

    def _test_query_table(self):
        with db_read() as db:
            rst = db.execute('SELECT count(*) FROM test_db;')
            # print(rst.fetchall())

            # assert rst.fetchall() == [(1,)]

    def _test_drop_table(self):
        with db_write() as db:
            rst = db.execute('DROP TABLE test_db;')


if __name__ == '__main__':
    unittest.main()
