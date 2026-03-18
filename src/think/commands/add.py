"""add 命令"""

import typer
import json
from datetime import datetime
from pathlib import Path
from ..core.models import Idea
from ..db import get_connection
from ..const import PRIORITIES, STATUSES
from dong import json_output, ValidationError
from rich.console import Console
from rich.table import Table

console = Console()


@json_output
def add(
    content: str = typer.Argument(..., help="想法内容"),
    tag: str = typer.Option(None, "--tag", "-t", help="标签，多个用逗号分隔"),
    priority: str = typer.Option("normal", "--priority", "-p",
                                   help="优先级: low/normal/high"),
    context: str = typer.Option(None, "--context", "-c", help="上下文"),
    source_agent: str = typer.Option(None, "--source", "-s", help="来源智能体"),
    note: str = typer.Option(None, "--note", "-n", help="备注"),
):
    """记录想法"""
    if not content or not content.strip():
        raise ValidationError("content", "想法内容不能为空")

    conn = get_connection()

    # 处理标签
    tags = []
    if tag:
        tags = [t.strip() for t in tag.split(",") if t.strip()]

    # 创建想法
    idea = Idea(
        content=content.strip(),
        tags=tags if tags else None,
        priority=priority,
        context=context,
        source_agent=source_agent,
        note=note,
    )

    # 插入数据库
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO ideas (content, tags, priority, context, source_agent, note, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            idea.content,
            json.dumps(idea.tags) if idea.tags else None,
            idea.priority,
            idea.context,
            idea.source_agent,
            idea.note,
            datetime.now().isoformat(),
            datetime.now().isoformat(),
        ),
    )
    conn.commit()

    idea_id = cursor.lastrowid
    conn.close()

    idea.id = idea_id
    return idea.to_dict()
