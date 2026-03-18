"""数据库连接管理模块

继承 dong.db.Database，提供 think-cli 专用数据库访问。
"""

import sqlite3
from typing import Iterator
from contextlib import contextmanager

from dong.db import Database as DongDatabase


class ThinkDatabase(DongDatabase):
    """思咚咚数据库类 - 继承自 dong.db.Database

    数据库路径: ~/.think/think.db
    """

    @classmethod
    def get_name(cls) -> str:
        """返回 CLI 名称"""
        return "think"


# 兼容性函数
def get_connection(db_path=None):
    return ThinkDatabase.get_connection()

def close_connection():
    ThinkDatabase.close_connection()

@contextmanager
def get_cursor() -> Iterator[sqlite3.Cursor]:
    with ThinkDatabase.get_cursor() as cur:
        yield cur

def get_db_path():
    return ThinkDatabase.get_db_path()
