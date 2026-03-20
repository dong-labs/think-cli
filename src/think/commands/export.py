"""导出命令"""
import typer
from rich.console import Console
from dong.io import ExporterRegistry
from think.exporter import ThinkExporter

console = Console()

def export(output: str = typer.Option("think.json", "-o", "--output"), format: str = typer.Option("json", "-f", "--format")):
    if not ExporterRegistry.get("think"):
        ExporterRegistry.register(ThinkExporter())
    exporter = ExporterRegistry.get("think")
    data = exporter.to_json() if format == "json" else exporter.to_markdown()
    with open(output, "w", encoding="utf-8") as f:
        f.write(data)
    console.print(f"✅ 已导出 {len(exporter.fetch_all())} 条灵感数据到 {output}", style="green")
