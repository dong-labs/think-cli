"""CLI 入口"""

import typer
from . import const

app = typer.Typer(
    name="think",
    help=f"思咚咚 - 记录灵感和想法 (v{const.VERSION})"
)

# 导入命令
from .commands import init, add, ls, get, delete, search, update, review, stats

app.command()(init.init)
app.command()(add.add)
app.command(name="list")(ls.list_ideas)
app.command()(get.get)
app.command()(delete.delete)
app.command()(search.search)
app.command()(update.update)
app.command()(review.review)
app.command()(stats.stats)

def main():
    app()

if __name__ == "__main__":
    main()
