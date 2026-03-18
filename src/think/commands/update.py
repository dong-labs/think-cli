"""update 命令"""

import typer
import json
from ..core.models import Idea
from ..db import get_connection
from ..const import PRIORITIES, STATUSES
from rich.console import Console

console = Console()


def update(
    idea_id: int = typer.Argument(..., help="想法 ID"),
    status: str = typer.Option(None, "--status", help="更新状态"),
    priority: str = typer.Option(None, "--priority", help="更新优先级: low/normal/high"),
    tag_add: str = typer.Option(None, "--add-tag", help="添加标签"),
    tag_remove: str = typer.Option(None, "--remove-tag", help="移除标签"),
    note: str = typer.Option(None, "--note", help="更新备注"),
):
    """更新想法

    Args:
        idea_id: 想法 ID
        status: 更新状态
        priority: 更新优先级
        tag_add: 添加标签
        tag_remove: 移除标签
        note: 更新备注
    """
    conn = get_connection()
    cursor = conn.cursor()

    # 获取当前想法
    cursor.execute("SELECT * FROM ideas WHERE id = ?", (idea_id,))
    row = cursor.fetchone()

    if not row:
        console.print(f"[red]❌ 未找到 ID 为 {idea_id} 的想法[/red]")
        conn.close()
        raise typer.Exit(code=1)

    idea = Idea.from_row(row)

    # 解析当前标签
    current_tags = idea.tags or []

    # 更新状态
    if status:
        if status not in STATUSES:
            console.print(f"[yellow]⚠️  无效的状态: {status}[/yellow]")
        else:
            idea.status = status

    # 更新优先级
    if priority:
        if priority not in PRIORITIES:
            console.print(f"[yellow]⚠️  无效的优先级: {priority}[/yellow]")
        else:
            idea.priority = priority

    # 添加标签
    if tag_add:
        new_tag = tag_add.strip()
        if new_tag and new_tag not in current_tags:
            current_tags.append(new_tag)
            idea.tags = current_tags

    # 移除标签
    if tag_remove:
        tag_to_remove = tag_remove.strip()
        if tag_to_remove in current_tags:
            current_tags.remove(tag_to_remove)
            idea.tags = current_tags if current_tags else None

    # 更新备注
    if note is not None:
        idea.note = note

    # 更新数据库
    cursor.execute(
        """
        UPDATE ideas
        SET tags = ?, priority = ?, status = ?, note = ?, updated_at = ?
        WHERE id = ?
        """,
        (
            json.dumps(current_tags) if current_tags else None,
            idea.priority,
            idea.status,
            idea.note,
            idea.updated_at,  # 会重新赋值
            idea_id,
        ),
    )
    conn.commit()
    conn.close()

    console.print(f"[green]✅ 已更新想法 #{idea_id}[/green]")
    if idea.status:
        console.print(f"    状态: {idea.status}")
    if idea.priority:
        console.print(f"    优先级: {idea.priority}")


if __name__ == "__main__":
    update()
