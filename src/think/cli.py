"""CLI 入口"""

import typer
from . import const

app = typer.Typer(
    name="think",
    help=f"思咚咚 - 记录灵感和想法 (v{const.VERSION})"
)

# 导入命令
from .commands import init, add, ls, get, delete, search, update, review, stats, tags, export, data_import

app.command()(init.init)
app.command()(add.add)
app.command(name="list")(ls.list_ideas)
app.command()(get.get)
app.command()(delete.delete)
app.command()(search.search)
app.command()(update.update)
app.command()(review.review)
app.command()(stats.stats)
app.command()(tags.tags)
app.command()(export.export)
app.command(name="import")(data_import.import_data)

def main():
    app()

if __name__ == "__main__":
    main()

@app.command()
def export(output: str = typer.Option("think.json", "-o", "--output"), format: str = typer.Option("json", "-f", "--format")):
    """导出数据"""
    from .commands.export import export as do_export
    do_export(output, format)

@app.command(name="import")
def import_data(file: str = typer.Option(..., "-f", "--file"), merge: bool = typer.Option(False, "--merge"), dry_run: bool = typer.Option(False, "--dry-run")):
    """导入数据"""
    from .commands.data_import import import_data as do_import
    do_import(file, merge, dry_run)
