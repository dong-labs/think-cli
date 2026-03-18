# 架构设计

## 技术栈

| 组件 | 选择 |
|------|------|
| 语言 | Python 3.11+ |
| CLI 框架 | Typer |
| 输出 | Rich |
| 数据库 | SQLite |

## 项目结构

```
ThinkDongDong/
├── src/think/
│   ├── cli.py           # CLI 入口
│   ├── const.py         # 常量定义
│   ├── core/
│   │   └── models.py    # 数据模型
│   ├── db/
│   │   └── connection.py # 数据库连接
│   └── commands/        # 命令实现
│       ├── init.py
│       ├── add.py
│       ├── ls.py
│       ├── get.py
│       ├── delete.py
│       ├── search.py
│       ├── update.py
│       ├── review.py
│       └── stats.py
├── agent/               # Agent workspace
└── tests/               # 测试
```

## 数据模型

```sql
CREATE TABLE ideas (
    id INTEGER PRIMARY KEY,
    content TEXT NOT NULL,
    tags TEXT,
    priority TEXT DEFAULT 'normal',
    status TEXT DEFAULT 'idea',
    context TEXT,
    source_agent TEXT,
    note TEXT,
    created_at TEXT,
    updated_at TEXT
);
```

## 设计原则

1. **简单优先** - SQLite 单文件，无需配置
2. **Agent 友好** - 所有命令支持 `--json` 输出
3. **本地私有** - 数据存储在用户本地
