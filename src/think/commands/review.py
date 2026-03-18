"""review 命令"""

import typer
import json
from datetime import datetime, timedelta
from ..core.models import Idea
from ..db import get_connection
from ..const import STATUSES, PRIORITIES, APP_NAME
from rich.console import Console
from rich.panel import Panel

console = Console()


def review(
    today: bool = typer.Option(False, "--today", help="只显示今天的想法"),
    week: bool = typer.Option(False, "--week", help="只显示本周的想法"),
    random: bool = typer.Option(False, "--random", help="随机显示一条想法"),
):
    """回顾想法

    Args:
        today: 只显示今天的想法
        week: 只显示本周的想法
        random: 随机显示一条想法
    """
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM ideas ORDER BY RANDOM() LIMIT 1"
    params = []

    if today:
        today_str = datetime.now().strftime("%Y-%m-%d")
        query = "SELECT * FROM ideas WHERE date(created_at) = ? ORDER BY RANDOM() LIMIT 1"
        params = [today_str]
    elif week:
        week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        query = "SELECT * FROM ideas WHERE date(created_at) >= ? ORDER BY RANDOM() LIMIT 1"
        params = [week_ago]

    cursor.execute(query, params)
    row = cursor.fetchone()
    conn.close()

    if not row:
        if today:
            console.print(f"[yellow]{APP_NAME} 今天还没有想法记录[/yellow]")
        elif week:
            console.print(f"[yellow]{APP_NAME} 本周还没有想法记录[/yellow]")
        else:
            console.print(f"[yellow]{APP_NAME} 还没有想法记录，快去记一条吧！💡[/yellow]")
        return

    idea = Idea.from_row(row)

    # 使用 Rich 显示
    console.print(Panel(
        f"{idea.content}\n\n[italic]#{idea.id} | {idea.created_at.split('T')[0]}[/italic]",
        title="💡 思考时间",
        title_align="left",
    ))

    if idea.tags:
        tags_str = ", ".join(idea.tags)
        console.print(f"[dim]标签: {tags_str}[/dim]")

    console.print(f"[dim]上下文: {idea.context or '无'}[/dim]")


if __name__ == "__main__":
    review()
