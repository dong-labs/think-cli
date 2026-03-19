"""tags 命令 - 列出所有标签及数量"""

import typer
import json
from collections import Counter
from ..db import get_connection
from rich.console import Console

console = Console()


def tags(
    json_output: bool = typer.Option(False, "--json", help="JSON 输出"),
):
    """列出所有标签及使用数量

    Args:
        json_output: JSON 输出
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT tags FROM ideas WHERE tags IS NOT NULL AND tags != ''")
    rows = cursor.fetchall()
    conn.close()

    # 统计标签
    tag_counter = Counter()
    for row in rows:
        try:
            tags_list = json.loads(row["tags"])
            if tags_list:
                tag_counter.update(tags_list)
        except (json.JSONDecodeError, TypeError):
            continue

    # 构建结果
    tags_list = [{"tag": tag, "count": count} for tag, count in tag_counter.most_common()]

    result = {
        "success": True,
        "data": {
            "total_tags": len(tag_counter),
            "total_usages": sum(tag_counter.values()),
            "tags": tags_list
        }
    }

    if json_output:
        console.print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    # 美化输出
    if not tags_list:
        console.print("[yellow]暂无标签[/yellow]")
        return

    from rich.table import Table
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("标签", style="green")
    table.add_column("数量", justify="right")

    for item in tags_list:
        table.add_row(item["tag"], str(item["count"]))

    console.print(table)
    console.print(f"\n总计: {len(tag_counter)} 个标签, {sum(tag_counter.values())} 次使用")


if __name__ == "__main__":
    tags()
