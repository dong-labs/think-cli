"""初始化命令"""

import typer
from rich.console import Console
from pathlib import Path
from ..db import init_database
from ..const import APP_NAME, VERSION, DATA_DIR

console = Console()

def init(
    db_path: Path = None,
    yes: bool = typer.Option(False, "--yes", "-y", help="不提示，直接初始化"),
):
    """初始化数据库

    Args:
        db_path: 数据库文件路径，默认使用 ~/.think/think.db
        yes: 不提示，直接初始化
    """
    if db_path is None:
        db_path = DATA_DIR / "think.db"

    # 检查是否已存在
    if db_path.exists():
        if not yes:
            confirm = typer.confirm(
                f"{db_path} 已存在，是否覆盖？",
                default=False,
            )
            if not confirm:
                console.print("[yellow]已取消初始化[/yellow]")
                return

    try:
        init_database(db_path)
        console.print(f"[green]✅ {APP_NAME} 初始化成功[/green]")
        console.print(f"    数据库路径: {db_path}")
        console.print(f"    版本: v{VERSION}")
    except Exception as e:
        console.print(f"[red]❌ 初始化失败: {e}[/red]")
        raise typer.Exit(code=1)
