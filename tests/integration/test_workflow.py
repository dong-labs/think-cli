"""测试工作流"""
import pytest
from typer.testing import CliRunner
from think.cli import app

runner = CliRunner()


def test_full_workflow():
    """测试完整工作流"""
    # 初始化
    result = runner.invoke(app, ["init", "--yes"])
    assert result.exit_code == 0

    # 记录想法
    result = runner.invoke(app, ["add", "工作流测试想法", "--tag", "test"])
    assert result.exit_code == 0

    # 列出
    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0

    # 搜索
    result = runner.invoke(app, ["search", "工作流"])
    assert result.exit_code == 0

    # 统计
    result = runner.invoke(app, ["stats"])
    assert result.exit_code == 0

    # 回顾
    result = runner.invoke(app, ["review"])
    assert result.exit_code == 0
