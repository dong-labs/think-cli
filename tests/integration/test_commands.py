"""测试 add 命令"""
import pytest
from typer.testing import CliRunner
from think.cli import app

runner = CliRunner()


def test_init():
    """测试初始化"""
    result = runner.invoke(app, ["init", "--yes"])
    assert result.exit_code == 0
    assert "初始化成功" in result.output


def test_add():
    """测试记录想法"""
    result = runner.invoke(app, ["add", "测试想法"])
    assert result.exit_code == 0
    assert "记录成功" in result.output


def test_list():
    """测试列出想法"""
    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0


def test_stats():
    """测试统计"""
    result = runner.invoke(app, ["stats"])
    assert result.exit_code == 0
    assert "统计" in result.output


def test_review():
    """测试回顾"""
    result = runner.invoke(app, ["review", "--week"])
    assert result.exit_code == 0
