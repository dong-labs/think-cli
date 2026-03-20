"""导入器模块"""
from typing import Any
from dong.io import BaseImporter, ImporterRegistry
from .db.connection import ThinkDatabase

class ThinkImporter(BaseImporter):
    name = "think"
    
    def validate(self, data: list[dict[str, Any]]) -> tuple[bool, str]:
        if not isinstance(data, list):
            return False, "数据必须是列表格式"
        for i, item in enumerate(data):
            if not isinstance(item, dict) or "content" not in item:
                return False, f"第 {i+1} 条数据缺少 content 字段"
        return True, ""
    
    def import_data(self, data: list[dict[str, Any]], merge: bool = False) -> dict[str, Any]:
        with ThinkDatabase.get_cursor() as cur:
            if not merge:
                cur.execute("DELETE FROM ideas")
            imported, skipped = 0, 0
            for item in data:
                if merge:
                    cur.execute("SELECT id FROM ideas WHERE content = ?", (item["content"],))
                    if cur.fetchone():
                        skipped += 1
                        continue
                cur.execute(
                    """INSERT INTO ideas (content, tags, priority, status, context, source_agent, note)
                       VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (item["content"], ",".join(item.get("tags", [])), item.get("priority", "normal"),
                     item.get("status", "idea"), item.get("context"), item.get("source_agent"), item.get("note"))
                )
                imported += 1
            return {"imported": imported, "skipped": skipped, "total": len(data)}

ImporterRegistry.register(ThinkImporter())
