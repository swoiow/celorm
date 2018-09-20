#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
http://alembic.zzzcomputing.com/en/latest/api/index.html
http://alembic.zzzcomputing.com/en/latest/api/commands.html
http://alembic.zzzcomputing.com/en/latest/api/config.html#alembic.config.Config
"""

from __future__ import absolute_import

import os.path as osph
import pdb
import pickle
import sys
import time


cPickle = pickle

sys.path.insert(0, osph.join(osph.abspath(osph.dirname(__file__)), osph.pardir))

_migration_path = osph.join(osph.curdir, ".alembic")
_base_path = osph.abspath(osph.dirname(__file__))

_origin_line = """# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = None"""

_new_line = """
# [start] celorm patch

from orm import OrmBase
target_metadata = OrmBase.metadata

import glob
from importlib.machinery import SourceFileLoader
from os.path import (join, realpath)

mods_map = {}

search_rules = [
    join(realpath("."), "*", "model.py"),
    join(realpath("."), "*", "models.py"),
]
print("当前搜索规则是: {}\n".format(search_rules))
mods = [glob.glob(ph) for ph in search_rules]

for idx, mod_ph in enumerate(mods):
    msg = mod_ph
    try:
        mod = SourceFileLoader("dynamic_imp_mod.{}".format(idx), mod_ph).load_module()

        for o in dir(mod):
            _obj = type(getattr(mod, o))
            if issubclass(_obj, OrmBase) and hasattr(_obj, "__tablename__"):
                mods_map[idx] = _obj

        msg = "成功加载模型: {}\n".format(mod_ph)

    except (Exception,) as e:
        msg = "加载模型时，出现错误。\n模型路径: {}\n" \
              "错误信息: {}\n".format(mod_ph, e)
    finally:
        print(msg)
        del msg
# [end] celorm patch
"""


class CLI(object):
    @staticmethod
    def init_db():
        if osph.exists(_migration_path):
            return _migration_path + " has existed!"

        else:
            from alembic import command
            from alembic.config import Config

            alembic_cfg = Config(
                file_="alembic.ini",
            )
            command.init(alembic_cfg, _migration_path, template='generic')

            # 修改 env.py 文件
            patch_env()

            print("请修改 alembic.ini 中 sqlalchemy.url 的值. ")

    @staticmethod
    def makemigrations():
        if osph.exists(_migration_path):
            from alembic import command
            from alembic.config import Config

            alembic_cfg = Config("alembic.ini")
            output = command.revision(
                alembic_cfg,
                message=str(int(time.time())),
                autogenerate=True,
            )

        else:
            return _migration_path + " not existed!"

    @staticmethod
    def migrate(revision="head"):
        if osph.exists(_migration_path):
            from alembic.config import Config
            from alembic import command

            alembic_cfg = Config("alembic.ini")
            # alembic_cfg.set_main_option("url", "sqlite:///database.db")  # for test

            output = command.upgrade(alembic_cfg, revision=revision)
            return output

        else:
            return _migration_path + " not existed!"

    # def auto_migrate(self):
    #     self.makemigrations()
    #     self.migrate()

    def __repr__(self):
        return "<{} @{}>".format(self.__class__.__name__, hex(id(self.__class__)))


def patch_env():
    from alembic.config import Config

    alembic_cfg = Config("alembic.ini")

    env_path = alembic_cfg.get_main_option("script_location")
    env_path = osph.join(env_path, "env.py")
    with open(env_path, "r") as rf:
        _origin_f = rf.read()

    with open(env_path, "w") as wf:
        _new_f = _origin_f.replace(_origin_line, _new_line)
        wf.write(_new_f)


def dump_check(file):
    if osph.isfile(file):
        with open(file, "rb") as rf:
            ctx = cPickle.load(rf)

        print("activate python pdb. please check the object(ctx)")
        pdb.set_trace()


def main():
    try:
        import fire

        inst = CLI()
        inst.dmp_chk = dump_check

        fire.Fire(inst)

    except ImportError:
        print(
            "running cli mode failed. "
            "missing fire. please install package with extra-cli or extra-full. "
            "to get more, check in github https://github.com/swoiow/celorm "
        )
