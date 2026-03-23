"""CLI 入口"""

import typer
from rich.console import Console
from dong import json_output
from . import const

console = Console()

app = typer.Typer(
    name="dong-think",
    help="思咚咚 - 记录灵感和想法",
    no_args_is_help=True,
    add_completion=False,
)


def version_callback(value: bool) -> None:
    """版本号回调函数"""
    if value:
        console.print(f"dong-think {const.VERSION}")
        raise typer.Exit()


@app.callback()
def global_options(
    version: bool = typer.Option(
        False,
        "--version",
        "-v",
        help="显示版本号",
        callback=version_callback,
        is_eager=True,
    ),
) -> None:
    """全局选项"""
    pass


@app.command()
@json_output
def init():
    """初始化数据库"""
    from .commands import init
    return init.init()


@app.command()
@json_output
def add(
    content: str = typer.Argument(..., help="想法内容"),
    tag: str = typer.Option(None, "--tag", "-t", help="标签"),
    priority: str = typer.Option("normal", "--priority", "-p", help="优先级"),
    context: str = typer.Option(None, "--context", "-c", help="上下文"),
):
    """记录想法"""
    from .commands import add
    return add.add(content=content, tag=tag, priority=priority, context=context)


@app.command()
@json_output
def list(
    limit: int = typer.Option(20, "--limit", "-l", help="返回数量"),
    tag: str = typer.Option(None, "--tag", "-t", help="按标签筛选"),
):
    """列出想法"""
    from .commands import ls
    return ls.list_ideas(limit=limit, tag=tag)


@app.command()
@json_output
def get(
    idea_id: int = typer.Argument(..., help="想法 ID"),
):
    """获取想法详情"""
    from .commands import get
    return get.get(idea_id=idea_id)


@app.command()
@json_output
def delete(
    idea_id: int = typer.Argument(..., help="想法 ID"),
):
    """删除想法"""
    from .commands import delete
    return delete.delete(idea_id=idea_id)


@app.command()
@json_output
def search(
    keyword: str = typer.Argument(..., help="搜索关键词"),
    limit: int = typer.Option(20, "--limit", "-l", help="返回数量"),
):
    """搜索想法"""
    from .commands import search
    return search.search(keyword=keyword, limit=limit)


@app.command()
@json_output
def update(
    idea_id: int = typer.Argument(..., help="想法 ID"),
    content: str = typer.Option(None, "--content", "-c", help="更新内容"),
    tag: str = typer.Option(None, "--tag", "-t", help="标签"),
):
    """更新想法"""
    from .commands import update
    return update.update(idea_id=idea_id, content=content, tag=tag)


@app.command()
@json_output
def review():
    """回顾想法"""
    from .commands import review
    return review.review()


@app.command()
@json_output
def stats():
    """统计信息"""
    from .commands import stats
    return stats.stats()


@app.command()
@json_output
def tags():
    """列出所有标签"""
    from .commands import tags
    return tags.tags()


@app.command()
def export(
    output: str = typer.Option("think.json", "-o", "--output", help="输出文件"),
    format: str = typer.Option("json", "-f", "--format", help="格式: json"),
):
    """导出数据"""
    from .commands import export as do_export
    do_export(output, format)


@app.command(name="import")
def import_data(
    file: str = typer.Option(..., "-f", "--file", help="导入文件"),
    merge: bool = typer.Option(False, "--merge", help="合并模式"),
    dry_run: bool = typer.Option(False, "--dry-run", help="预览模式"),
):
    """导入数据"""
    from .commands import data_import
    return data_import.import_data(file=file, merge=merge, dry_run=dry_run)


if __name__ == "__main__":
    app()
