# What
Sqlalchemy + alembic => django-orm

# How
default search: model.py & models.py
```
>> myorm
Type:        Help
String form: <Help @0x24db5d36168>
File:        ......
Docstring:   帮助函数

Usage:       myorm
             myorm init-db
             myorm makemigrations
             myorm migrate
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