#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
http://alembic.zzzcomputing.com/en/latest/api/index.html
http://alembic.zzzcomputing.com/en/latest/api/commands.html
http://alembic.zzzcomputing.com/en/latest/api/config.html#alembic.config.Config
"""

from __future__ import absolute_import

import pickle
import sys
import time
from os import path

from colorama import Fore, init


init(autoreset=True)

cPickle = pickle

sys.path.insert(0, path.join(path.abspath(path.dirname(__file__)), path.pardir))

_migration_path = path.join(path.curdir, ".alembic")
_package_dir = path.abspath(path.dirname(__file__))

sp_search_models = "search_models.ptpl"

_origin_line = """# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = None"""

_new_line = r"""
# [start] celorm patch. Don't remove this line.
from os import path
from celorm.utils import OrmBase
from importlib.machinery import SourceFileLoader

target_metadata = OrmBase.metadata
mods_map = {}

main_dir = config.get_main_option("script_location")
sp_path = path.join(main_dir, "search_models.py")
script = SourceFileLoader("search_models", sp_path).load_module()

# [end] celorm patch. Don't remove this line.
"""


class CLI(object):
    """ A database manager tools just like django-orm. """

    @staticmethod
    def init_db():
        if path.exists(_migration_path):
            print(Fore.YELLOW + _migration_path + " has existed!")
            return

        else:
            from alembic import command
            from alembic.config import Config

            alembic_cfg = Config(
                file_="alembic.ini",
            )

            command.init(alembic_cfg, _set_unix_path(_migration_path), template="generic")

            # 修改 env.py 文件
            patch_env()

            print("\n" + Fore.YELLOW +
                  "请修改 alembic.ini 中 sqlalchemy.url 的值. \n"
                  "请修改 .alembic/search_models.py 中 search_rules 的路径. \n")

    @staticmethod
    def makemigrations():
        if path.exists(_migration_path):
            from alembic import command
            from alembic.config import Config

            alembic_cfg = Config("alembic.ini")
            command.revision(
                alembic_cfg,
                message=str(int(time.time())),
                autogenerate=True,
            )

        else:
            print(Fore.YELLOW + _migration_path + " not existed!")

            return

    @staticmethod
    def migrate(revision="head"):
        if path.exists(_migration_path):
            from alembic.config import Config
            from alembic import command

            alembic_cfg = Config("alembic.ini")
            # alembic_cfg.set_main_option("url", "sqlite:///database.db")  # for test

            output = command.upgrade(alembic_cfg, revision=revision)
            return output

        else:
            print(Fore.YELLOW + _migration_path + " not existed!")

            return

    # def auto_migrate(self):
    #     self.makemigrations()
    #     self.migrate()

    def __repr__(self):
        return "<{} @{}>".format(self.__class__.__name__, hex(id(self.__class__)))


def patch_env():
    from alembic.config import Config
    from alembic.script.base import ScriptDirectory

    alembic_cfg = Config("alembic.ini")

    main_dir = alembic_cfg.get_main_option("script_location")
    main_dir = _set_unix_path(main_dir)

    env_path = path.join(main_dir, "env.py")
    with open(env_path, "r") as rf:
        _origin_f = rf.read()

    with open(env_path, "w") as wf:
        _new_f = _origin_f.replace(_origin_line, _new_line)
        wf.write(_new_f)

    script = ScriptDirectory(main_dir)
    script._copy_file(
        path.join(_package_dir, sp_search_models),
        path.join(main_dir, "search_models.py")
    )


def dump_check(file):
    import pdb

    if path.isfile(file):
        with open(file, "rb") as rf:
            ctx = cPickle.load(rf)

        print(Fore.BLUE + "activate python pdb. please check the object(ctx)")
        pdb.set_trace()


def search_models():
    """ running search models function in .alembic/env.py """

    from alembic.config import Config

    alembic_cfg = Config("alembic.ini")
    main_dir = alembic_cfg.get_main_option("script_location")
    main_dir = _set_unix_path(main_dir)

    if path.exists(main_dir):
        import importlib.util

        sp_path = path.join(main_dir, "search_models.py")

        spec = importlib.util.spec_from_file_location("search_models", sp_path)
        script = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(script)
        # f._search_models()
        message = "[I] 搜索完成。"

    else:
        message = "[W] 没找到 .alembic 文件夹。"

    print(Fore.YELLOW + message.strip() + "\n")

    return


def _set_unix_path(dir_):
    """ format alembic path in unix path. """
    nt_slash = "\\"
    unix_slash = "/"

    return dir_.replace(nt_slash, unix_slash)


def main():
    try:
        import fire

        inst = CLI()
        inst.dmp_chk = dump_check
        inst.search_models = search_models

        fire.Fire(inst)

    except ImportError as e:
        if e.name in ["fire"]:
            import sys

            message = "running cli mode failed. \n" \
                      "missing fire. please install package with extra-cli or extra-full. \n" \
                      "to get more, check in github https://github.com/swoiow/celorm \n"

            print(Fore.RED + message)
            return

        else:
            raise ImportError(e)
