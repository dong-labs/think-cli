"""delete 命令"""

import typer
import json
from ..core.models import Idea
from ..db import get_connection
from dong import json_output, NotFoundError
from rich.console import Console

console = Console()

@json_output
def delete(
    idea_id: int = typer.Argument(..., help="想法 ID"),
    force: bool = typer.Option(False, "--force", "-f", help="强制删除，不提示"),
):
    """删除想法

    Args:
        idea_id: 想法 ID
        force: 强制删除，不提示
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ideas WHERE id = ?", (idea_id,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        raise NotFoundError("Idea", idea_id, message=f"未找到 ID 为 {idea_id} 的想法")

    idea = Idea.from_row(row)

    if not force:
        confirm = typer.confirm(f"确定要删除想法吗？\n{idea.content}")
        if not confirm:
            conn.close()
            return {"cancelled": True, "message": "已取消删除"}

    cursor.execute("DELETE FROM ideas WHERE id = ?", (idea_id,))
    conn.commit()
    conn.close()

    return {"deleted": True, "id": idea_id}


if __name__ == "__main__":
    delete()
