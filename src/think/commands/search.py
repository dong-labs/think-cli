"""search 命令"""

import typer
import json
from ..core.models import Idea
from ..db import get_connection
from ..const import PRIORITIES, STATUSES
from rich.console import Console
from rich.table import Table

console = Console()


def search(
    keyword: str = typer.Argument(..., help="搜索关键词"),
    tag: str = typer.Option(None, "--tag", help="按标签筛选"),
    priority: str = typer.Option(None, "--priority", help="按优先级筛选: low/normal/high"),
    status: str = typer.Option(None, "--status", help="按状态筛选"),
    json_output: bool = typer.Option(False, "--json", help="JSON 输出"),
):
    """搜索想法

    Args:
        keyword: 搜索关键词
        tag: 按标签筛选
        priority: 按优先级筛选
        status: 按状态筛选
        json_output: JSON 输出
    """
    conn = get_connection()
    cursor = conn.cursor()

    # 构建查询条件
    conditions = ["content LIKE ?"]  # 关键词搜索
    params = [f"%{keyword}%"]

    if tag:
        conditions.append("tags LIKE ?")
        params.append(f"%{tag}%")

    if priority:
        if priority not in PRIORITIES:
            console.print(f"[yellow]⚠️  无效的优先级: {priority}[/yellow]")
        else:
            conditions.append("priority = ?")
            params.append(priority)

    if status:
        if status not in STATUSES:
            console.print(f"[yellow]⚠️  无效的状态: {status}[/yellow]")
        else:
            conditions.append("status = ?")
            params.append(status)

    where_clause = " AND ".join(conditions) if conditions else "1=1"

    query = f"""
        SELECT * FROM ideas
        WHERE {where_clause}
        ORDER BY created_at DESC
    """

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    if json_output:
        ideas = [Idea.from_row(row).to_dict() for row in rows]
        console.print(json.dumps(ideas, ensure_ascii=False, indent=2))
        return

    if not rows:
        console.print(f"[yellow]未找到包含 '{keyword}' 的想法[/yellow]")
        return

    # 创建表格
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", width=6)
    table.add_column("内容", width=40)
    table.add_column("标签", width=20)
    table.add_column("时间", style="dim")

    for row in rows:
        idea = Idea.from_row(row)
        tags_str = ", ".join(idea.tags) if idea.tags else ""
        time_str = idea.created_at.split("T")[0] if idea.created_at else ""

        table.add_row(
            str(idea.id),
            idea.content[:40] + "..." if len(idea.content) > 40 else idea.content,
            tags_str[:20],
            time_str,
        )

    console.print(table)
    console.print(f"[dim]找到 {len(rows)} 条结果[/dim]")


if __name__ == "__main__":
    search()
