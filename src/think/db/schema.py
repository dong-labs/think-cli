"""数据库 Schema 定义和版本管理

继承 dong.db.SchemaManager，管理 think-cli 的数据库 schema。
"""

from dong.db import SchemaManager
from .connection import ThinkDatabase

SCHEMA_VERSION = "1.0.0"


class ThinkSchemaManager(SchemaManager):
    """思咚咚 Schema 管理器"""

    def __init__(self):
        super().__init__(
            db_class=ThinkDatabase,
            current_version=SCHEMA_VERSION
        )

    def init_schema(self) -> None:
        self._create_thoughts_table()
        self._create_indexes()

    def _create_thoughts_table(self) -> None:
        with ThinkDatabase.get_cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS thoughts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    tags TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)

    def _create_indexes(self) -> None:
        with ThinkDatabase.get_cursor() as cur:
            cur.execute("CREATE INDEX IF NOT EXISTS idx_thoughts_tags ON thoughts(tags)")


# 兼容性函数
def get_schema_version() -> str | None:
    return ThinkSchemaManager().get_stored_version()

def set_schema_version(version: str) -> None:
    ThinkDatabase.set_meta(ThinkSchemaManager.VERSION_KEY, version)

def is_initialized() -> bool:
    return ThinkSchemaManager().is_initialized()

def init_database() -> None:
    schema = ThinkSchemaManager()
    if not schema.is_initialized():
        schema.initialize()
