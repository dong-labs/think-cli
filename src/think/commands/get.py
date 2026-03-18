"""get 命令"""

import typer
import json
from ..core.models import Idea
from ..db import get_connection
from dong import json_output, NotFoundError
from rich.console import Console

console = Console()

@json_output
def get(
    idea_id: int = typer.Argument(..., help="想法 ID"),
):
    """获取想法详情

    Args:
        idea_id: 想法 ID    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ideas WHERE id = ?", (idea_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise NotFoundError("Idea", idea_id, message=f"未找到 ID 为 {idea_id} 的想法")

    idea = Idea.from_row(row)
    return idea.to_dict()


if __name__ == "__main__":
    get()
