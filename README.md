# What
Sqlalchemy + alembic => django-orm


# How
+ utils only (without extras)
> `pip install https://github.com/swoiow/celorm/archive/master.zip`

+ with fire
> `pip install git+https://github.com/swoiow/celorm.git#egg=celorm[cli]`

+ with fire+alembic
> `pip install git+https://github.com/swoiow/celorm.git#egg=celorm[full]`

default search: model.py & models.py 
```
>> celorm

Type:        CLI
String form: <CLI @0x1f0ef118368>
File:        ...

Usage:       celorm
             celorm dmp-chk
             celorm init-db
             celorm makemigrations
             celorm migrate
```


# More

### dynamic_table
```
"""
http://windrocblog.sinaapp.com/?p=1554
http://docs.sqlalchemy.org/en/latest/orm/extensions/declarative/mixins.html
"""

from myorm.utils import OrmBase

record_table_mapper = {}
class PotentialModel(OrmBase):
    __tablename__ = "test-table"
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String(1000))

table = dynamic_table("PotentialModel", PotentialModel, "PotentialModel")
record_table_mapper["dyt_A"] = table

engine = sa.create_engine("sqlite:///database.db")
session = Session(bind=engine)

OrmBase.metadata.create_all(engine)

with db_write(engine) as db:
    b = table(name="abc123")
    db.add(b)
    c = table(name="qqq321")
    db.add(c)

with db_read(engine) as db:
    q = db.query(a)
    print(q.all())
```


# Note

+ SQLITE (http://docs.sqlalchemy.org/en/latest/dialects/sqlite.html):
```
# relative path
e = create_engine('sqlite:///path/to/database.db')
# absolute path
e = create_engine('sqlite:////path/to/database.db')
# absolute path on Windows
e = create_engine('sqlite:///C:\\path\\to\\database.db')
# in-memory database
e = create_engine('sqlite://')
```

+ MYSQL (http://docs.sqlalchemy.org/en/latest/dialects/mysql.html): 
```
mysql+mysqldb://{username}:{password}@{sql_host}:3306/{db_name}
mysql+pymysql://{username}:{password}@{sql_host}:3306/{db_name}[?<options>]
mysql+pyodbc://{username}:{password}@{dsnname}
```

+ MSSQL (http://docs.sqlalchemy.org/en/latest/dialects/mssql.html):
``` 
https://github.com/mkleehammer/pyodbc/wiki/Install
https://www.microsoft.com/zh-CN/download/details.aspx?id=53339
https://docs.microsoft.com/zh-cn/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-2017

DRIVER_NAME = "ODBC Driver 13 for SQL Server"
if sys.platform == "win32":
    DRIVER_NAME = "SQL Server"
"mssql+pyodbc://{username}:{password}@{sql_host}:1433/{db_name}?driver=" + DRIVER_NAME
```

+ POSTGRESQL (http://docs.sqlalchemy.org/en/latest/dialects/postgresql.html):
```
postgresql+psycopg2://{username}:{password}@{sql_host}:5432/{db_name}[?key=value&key=value...]
```

+ ORACLE (http://docs.sqlalchemy.org/en/latest/dialects/oracle.html):
```
http://www.oracle.com/technetwork/database/database-technologies/instant-client/cloud-3080565.html

set TNS_ADMIN=C:\oracle\instantclient_12_2
set NLS_LANG=SIMPLIFIED CHINESE_CHINA.UTF8
```


# LICENSE
*MPL-2.0*
