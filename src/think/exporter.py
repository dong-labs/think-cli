"""导出器模块"""
from typing import Any
from dong.io import BaseExporter, ExporterRegistry
from .db.connection import ThinkDatabase

class ThinkExporter(BaseExporter):
    name = "think"
    
    def fetch_all(self) -> list[dict[str, Any]]:
        with ThinkDatabase.get_cursor() as cur:
            cur.execute("""
                SELECT id, content, tags, priority, status, context, 
                       source_agent, note, created_at, updated_at
                FROM ideas ORDER BY created_at DESC
            """)
            return [
                {
                    "id": row[0], "content": row[1], "tags": row[2].split(",") if row[2] else [],
                    "priority": row[3], "status": row[4], "context": row[5],
                    "source_agent": row[6], "note": row[7],
                    "created_at": row[8], "updated_at": row[9],
                }
                for row in cur.fetchall()
            ]

ExporterRegistry.register(ThinkExporter())
