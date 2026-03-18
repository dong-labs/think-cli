# 思咚咚 - 实施计划

## 项目信息

| 项目 | 值 |
|------|-----|
| 中文名 | 思咚咚 |
| 英文 ID | think |
| CLI 包名 | think-cli |
| CLI 命令 | think |
| 数据目录 | ~/.think/ |
| 项目目录 | repos/ThinkDongDong/ |

---

## Phase 1: CLI 核心（1周）

### Day 1-2: 项目初始化 + 数据层

| 任务 | 文件 | 状态 |
|------|------|------|
| 创建项目结构 | - | ⬜ |
| pyproject.toml | pyproject.toml | ⬜ |
| 常量定义 | src/think/const.py | ⬜ |
| 数据库连接 | src/think/db/connection.py | ⬜ |
| Schema 定义 | src/think/db/schema.py | ⬜ |
| 数据模型 | src/think/core/models.py | ⬜ |
| init 命令 | src/think/commands/init.py | ⬜ |

### Day 3-4: 核心 CRUD 命令

| 任务 | 文件 | 状态 |
|------|------|------|
| add 命令 | src/think/commands/add.py | ⬜ |
| ls 命令 | src/think/commands/ls.py | ⬜ |
| get 命令 | src/think/commands/get.py | ⬜ |
| delete 命令 | src/think/commands/delete.py | ⬜ |
| CLI 入口 | src/think/cli.py | ⬜ |

### Day 5-7: 搜索 + 增强

| 任务 | 文件 | 状态 |
|------|------|------|
| search 命令 | src/think/commands/search.py | ⬜ |
| update 命令 | src/think/commands/update.py | ⬜ |
| review 命令 | src/think/commands/review.py | ⬜ |
| stats 命令 | src/think/commands/stats.py | ⬜ |
| JSON 输出 | 各命令 --json 参数 | ⬜ |
| 单元测试 | tests/unit/ | ⬜ |
| 集成测试 | tests/integration/ | ⬜ |

---

## Phase 2: Agent Workspace（1周）

### Day 8-10: Agent 定义

| 任务 | 文件 | 状态 |
|------|------|------|
| IDENTITY.md | agent/IDENTITY.md | ⬜ |
| SOUL.md | agent/SOUL.md | ⬜ |
| TOOLS.md | agent/TOOLS.md | ⬜ |
| USER.md | agent/USER.md | ⬜ |
| OVERVIEW.md | agent/OVERVIEW.md | ⬜ |
| MEMORY.md.template | agent/MEMORY.md.template | ⬜ |

### Day 11-14: 文档 + 发布

| 任务 | 文件 | 状态 |
|------|------|------|
| README.md | README.md | ⬜ |
| ARCHITECTURE.md | ARCHITECTURE.md | ⬜ |
| WHY.md | WHY.md | ⬜ |
| API_REFERENCE.md | docs/API_REFERENCE.md | ⬜ |
| 发布到 PyPI | - | ⬜ |

---

## 技术要点

### CLI 入口

```python
# src/think/cli.py
import typer

app = typer.Typer(name="think", help="思咚咚 - 记录灵感和想法")

@app.command()
def add(content: str, tag: list[str] = None, priority: str = "normal"):
    """记录想法"""
    ...

@app.command()  
def ls(today: bool = False, tag: str = None):
    """列出想法"""
    ...
```

### pyproject.toml

```toml
[project]
name = "think-cli"
version = "0.1.0"

[project.scripts]
think = "think.cli:app"
```

### 数据库

```python
# ~/.think/think.db
# 首次运行 think init 时创建
```

---

## 验收标准

### CLI

- [ ] `think init` 初始化数据库
- [ ] `think add "xxx"` 记录想法
- [ ] `think ls` 列出想法
- [ ] `think get 1` 获取详情
- [ ] `think search "xxx"` 搜索
- [ ] `think update 1 --status todo` 更新
- [ ] `think delete 1` 删除
- [ ] `think review --week` 回顾
- [ ] `think stats` 统计
- [ ] 所有命令支持 `--json` 输出

### Agent

- [ ] Agent 能调用 CLI 记录想法
- [ ] Agent 能搜索想法
- [ ] Agent 能回顾想法

---

*2026-03-15*
