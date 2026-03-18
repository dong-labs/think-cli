"""stats 命令"""

import json
from datetime import datetime, timedelta
from ..core.models import Idea
from ..db import get_connection
from ..const import APP_NAME, PRIORITIES, STATUSES
from rich.console import Console
from rich.table import Table
from rich.progress import Progress

console = Console()


def stats():
    """统计想法信息"""
    conn = get_connection()
    cursor = conn.cursor()

    # 总数
    cursor.execute("SELECT COUNT(*) FROM ideas")
    total = cursor.fetchone()[0]

    # 按状态统计
    cursor.execute("""
        SELECT status, COUNT(*) as count
        FROM ideas
        GROUP BY status
    """)
    status_stats = {row["status"]: row["count"] for row in cursor.fetchall()}

    # 按优先级统计
    cursor.execute("""
        SELECT priority, COUNT(*) as count
        FROM ideas
        GROUP BY priority
    """)
    priority_stats = {row["priority"]: row["count"] for row in cursor.fetchall()}

    # 最近7天
    week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    cursor.execute("SELECT COUNT(*) FROM ideas WHERE date(created_at) >= ?", [week_ago])
    this_week = cursor.fetchone()[0]

    # 最近30天
    month_ago = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    cursor.execute("SELECT COUNT(*) FROM ideas WHERE date(created_at) >= ?", [month_ago])
    this_month = cursor.fetchone()[0]

    conn.close()

    # 显示统计表
    table = Table(title=f"📊 {APP_NAME} 统计", show_header=True, header_style="bold magenta")
    table.add_column("指标", style="cyan")
    table.add_column("数值", style="bold green")

    table.add_row("总想法数", str(total))
    table.add_row("本周新增", str(this_week))
    table.add_row("本月新增", str(this_month))
    table.add_row("", "")

    # 状态统计
    for status in STATUSES:
        count = status_stats.get(status, 0)
        if count > 0:
            table.add_row(f"  - {status}", str(count))

    table.add_row("", "")

    # 优先级统计
    for priority in PRIORITIES:
        count = priority_stats.get(priority, 0)
        if count > 0:
            table.add_row(f"  - {priority}", str(count))

    console.print(table)

    # 显示建议
    if total == 0:
        console.print(f"\n💡 提示: 还没有想法记录，快去记一条吧！")
    elif this_week == 0:
        console.print(f"\n💡 提示: 本周还没有想法记录，快去记一条吧！")
    else:
        console.print(f"\n💡 提示: 记录想法，让你的思考有迹可循！")


if __name__ == "__main__":
    stats()
