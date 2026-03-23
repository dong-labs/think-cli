"""ls 命令"""

import typer
import json
from datetime import datetime
from ..core.models import Idea
from ..db import get_connection
from ..const import DEFAULT_LIMIT, PRIORITIES, STATUSES
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


def _is_option_info(value):
    """检查是否是 Typer OptionInfo 对象"""
    return hasattr(value, '__class__') and value.__class__.__name__ == 'OptionInfo'


def list_ideas(
    limit: int = typer.Option(DEFAULT_LIMIT, "--limit", "-l", help="显示数量"),
    today: bool = typer.Option(False, "--today", help="只显示今天的"),
    week: bool = typer.Option(False, "--week", help="只显示本周的"),
    tag: str = typer.Option(None, "--tag", help="按标签筛选"),
    priority: str = typer.Option(None, "--priority", help="按优先级筛选: low/normal/high"),
    status: str = typer.Option(None, "--status", help="按状态筛选"),
    json_output: bool = typer.Option(False, "--json", help="JSON 输出"),
):
    """列出想法

    Args:
        limit: 显示数量
        today: 只显示今天的
        week: 只显示本周的
        tag: 按标签筛选
        priority: 按优先级筛选
        status: 按状态筛选
        json_output: JSON 输出
    """
    # 过滤 OptionInfo 对象
    if _is_option_info(priority):
        priority = None
    if _is_option_info(status):
        status = None

    conn = get_connection()
    cursor = conn.cursor()

    # 构建查询条件
    conditions = []
    params = []

    if today:
        today_str = datetime.now().strftime("%Y-%m-%d")
        conditions.append("date(created_at) = ?")
        params.append(today_str)

    if week:
        from datetime import timedelta
        week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        conditions.append("date(created_at) >= ?")
        params.append(week_ago)

    if tag:
        conditions.append("tags LIKE ?")
        params.append(f"%{tag}%")

    if priority:
        if priority not in PRIORITIES:
            console.print(f"[yellow]⚠️  无效的优先级: {priority}[/yellow]")
            priority = None
        else:
            conditions.append("priority = ?")
            params.append(priority)

    if status:
        if status not in STATUSES:
            console.print(f"[yellow]⚠️  无效的状态: {status}[/yellow]")
            status = None
        else:
            conditions.append("status = ?")
            params.append(status)

    where_clause = " AND ".join(conditions) if conditions else "1=1"
    params.extend([limit, 0])  # limit 和 offset

    query = f"""
        SELECT * FROM ideas
        WHERE {where_clause}
        ORDER BY created_at DESC
        LIMIT ? OFFSET ?
    """

    cursor.execute(query, params)
    rows = cursor.fetchall()

    if json_output:
        ideas = [Idea.from_row(row).to_dict() for row in rows]
        console.print(json.dumps(ideas, ensure_ascii=False, indent=2))
        return

    if not rows:
        console.print("[yellow]没有想法记录[/yellow]")
        return

    # 创建表格
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", width=6)
    table.add_column("内容", width=40)
    table.add_column("标签", width=20)
    table.add_column("优先级", width=10)
    table.add_column("状态", width=10)
    table.add_column("时间", style="dim")

    for row in rows:
        idea = Idea.from_row(row)
        tags_str = ", ".join(idea.tags) if idea.tags else ""
        time_str = idea.created_at.split("T")[0] if idea.created_at else ""

        # 根据优先级设置颜色
        priority_style = {
            "high": "bold red",
            "normal": "bold white",
            "low": "yellow",
        }.get(idea.priority, "")

        # 根据状态设置颜色
        status_style = {
            "done": "green",
            "doing": "cyan",
            "todo": "yellow",
            "idea": "dim",
        }.get(idea.status, "")

        table.add_row(
            str(idea.id),
            idea.content[:40] + "..." if len(idea.content) > 40 else idea.content,
            tags_str[:20],
            f"[{priority_style}]{idea.priority}[/{priority_style}]" if priority_style else idea.priority,
            f"[{status_style}]{idea.status}[/{status_style}]" if status_style else idea.status,
            time_str,
        )

    # 统计信息（使用同一个连接）
    total = conn.execute("SELECT COUNT(*) FROM ideas").fetchone()[0]
    console.print(f"\n总计: {total} 条想法")

    conn.close()


if __name__ == "__main__":
    list_ideas()
