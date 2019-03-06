#!/usr/bin/env python
# -*- coding: utf-8 -*-

__doc__ = """
doc:

+ SQLITE(http://docs.sqlalchemy.org/en/latest/dialects/sqlite.html):
# relative path
e = create_engine('sqlite:///path/to/database.db')
# absolute path
e = create_engine('sqlite:////path/to/database.db')
# absolute path on Windows
e = create_engine('sqlite:///C:\\path\\to\\database.db')
# in-memory database
e = create_engine('sqlite://')
=====

+ MYSQL(http://docs.sqlalchemy.org/en/latest/dialects/mysql.html): 
mysql+mysqldb://{username}:{password}@{sql_host}:3306/{db_name}
mysql+pymysql://{username}:{password}@{sql_host}:3306/{db_name}[?<options>]
mysql+pyodbc://{username}:{password}@{dsnname}
=====

+ MSSQL(http://docs.sqlalchemy.org/en/latest/dialects/mssql.html):
''' 
https://github.com/mkleehammer/pyodbc/wiki/Install
https://www.microsoft.com/zh-CN/download/details.aspx?id=53339
https://docs.microsoft.com/zh-cn/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-2017
'''

DRIVER_NAME = "ODBC Driver 13 for SQL Server"
if sys.platform == "win32":
    DRIVER_NAME = "SQL Server"
"mssql+pyodbc://{username}:{password}@{sql_host}:1433/{db_name}?driver=" + DRIVER_NAME
=====

+ POSTGRESQL(http://docs.sqlalchemy.org/en/latest/dialects/postgresql.html:
postgresql+psycopg2://{username}:{password}@{sql_host}:5432/{db_name}[?key=value&key=value...]
=====

+ ORACLE(http://docs.sqlalchemy.org/en/latest/dialects/oracle.html):
'''
http://www.oracle.com/technetwork/database/database-technologies/instant-client/cloud-3080565.html
'''
set TNS_ADMIN=C:\oracle\instantclient_12_2
set NLS_LANG=SIMPLIFIED CHINESE_CHINA.UTF8
- - - - - - - - - - - - - - - - - - - - 

You the better set a environment variables name DATABASE_URI.
if you want to hidden the doc, set a environment 'LIB_DOC=1'. 
"""

import os

from .utils import create_engine, db_read, db_write


if not os.environ.get("DATABASE_URI") and int(os.environ.get("LIB_DOC", 0)):
    print(__doc__)
