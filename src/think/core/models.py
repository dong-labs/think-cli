"""数据模型"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from ..const import PRIORITIES, STATUSES


class Idea:
    """想法模型"""

    def __init__(
        self,
        id: Optional[int] = None,
        content: str = "",
        tags: Optional[List[str]] = None,
        priority: str = "normal",
        status: str = "idea",
        context: Optional[str] = None,
        source_agent: Optional[str] = None,
        note: Optional[str] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
    ):
        self.id = id
        self.content = content
        self.tags = tags or []
        self.priority = priority
        self.status = status
        self.context = context
        self.source_agent = source_agent
        self.note = note
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def from_row(cls, row) -> "Idea":
        """从数据库行创建实例"""
        tags = None
        if row["tags"]:
            import json
            tags = json.loads(row["tags"])

        return cls(
            id=row["id"],
            content=row["content"],
            tags=tags,
            priority=row["priority"],
            status=row["status"],
            context=row["context"],
            source_agent=row["source_agent"],
            note=row["note"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        import json
        return {
            "id": self.id,
            "content": self.content,
            "tags": self.tags,
            "priority": self.priority,
            "status": self.status,
            "context": self.context,
            "source_agent": self.source_agent,
            "note": self.note,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Idea":
        """从字典创建实例"""
        return cls(**data)

    def validate(self) -> bool:
        """验证数据"""
        if not self.content or not self.content.strip():
            return False
        if self.priority not in PRIORITIES:
            self.priority = PRIORITY_NORMAL
        if self.status not in STATUSES:
            self.status = STATUS_IDEA
        return True
