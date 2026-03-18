# 思咚咚 (Si) - 设计方案

> 专注记录灵感和思考的智能体

---

## 1. 产品定位

### 核心诉求

```
和智能体聊天时，突然有个想法
    ↓
传统方式：打开笔记软件，记录
    ↓
问题：智能体不知道你记录了什么
    ↓
思咚咚：一句话记录，智能体可见
```

### 和阅咚咚的区别

| | 阅咚咚 | 思咚咚 |
|---|--------|--------|
| 内容 | 阅读摘录、文章收藏 | 灵感、想法、思考 |
| 来源 | 外部（文章、书） | 内部（你的大脑） |
| 特点 | 被动收集 | 主动记录 |
| 价值 | 知识积累 | 创意孵化 |

### 核心价值

- **即时** - 想法来了，一句话记录
- **可见** - 所有智能体能访问你的思考
- **回顾** - 定期提醒，不让想法沉睡

---

## 2. CLI 设计

### 包名

```
think-cli
命令：think
数据：~/.think/think.db
```

### 命令

```bash
# 初始化
think init

# 记录想法
think add "Agent Hub 可以去中心化"
think add "想法：用 IPFS 存 Agent 包" --tag agenthub,decentralized
think add "关于 Agent 互操作的思考" --tag agent --priority high

# 列出
think ls                    # 默认 20 条
think ls --today            # 今天
think ls --week             # 本周
think ls --tag agenthub     # 按标签
think ls --priority high    # 按优先级
think ls --status idea      # 按状态

# 搜索
think search "去中心化"
think search "agent" --tag agenthub

# 获取详情
think get 123

# 更新
think update 123 --status todo
think update 123 --tag +important

# 删除
think delete 123 --force

# 回顾
think review --today        # 今天想法
think review --week         # 本周想法
think review --random       # 随机一条

# 统计
think stats                 # 想法统计
```

### 输出格式

```bash
# JSON 输出（Agent 友好）
think add "xxx" --json

# 示例输出
{
  "success": true,
  "data": {
    "id": 1,
    "content": "Agent Hub 可以去中心化",
    "tags": [],
    "priority": "normal",
    "status": "idea",
    "created_at": "2026-03-15T09:50:00"
  }
}
```

---

## 3. Agent 设计

### 身份

```yaml
name: 思咚咚
id: si
species: 小灯泡 💡
role: 灵感和思考记录助手
```

### 性格

| 特质 | 说明 |
|------|------|
| **好奇** | 喜欢追问，帮你把想法变清晰 |
| **敏捷** | 快速记录，不打断心流 |
| **提醒** | 定期提醒你回顾旧想法 |

### 口癖

| 场景 | 口癖 |
|------|------|
| 记录成功 | "记下来了！💡" |
| 有趣的想法 | "这个想法有点意思..." |
| 追问 | "要不要展开说说？" |
| 回顾提醒 | "主人，要不要看看上周的想法？" |
| 发现关联 | "诶，这个和之前的 xxx 有点像" |

### 能力

| 能力 | 触发 | 行为 |
|------|------|------|
| 记录 | "记一下 xxx" | 提取内容，调用 `think add` |
| 快速记录 | "xxx"（简短） | 直接记录，不追问 |
| 追问 | 记录后 | "要不要加个标签？" |
| 检索 | "我有想过 xxx 吗" | 调用 `think search` |
| 回顾 | "回顾一下" | 调用 `think review` |
| 统计 | "我有多少想法" | 调用 `think stats` |

### 命令映射

| 用户表达 | 意图 | CLI 命令 |
|----------|------|----------|
| "记一下 xxx" | 记录想法 | `think add "xxx"` |
| "今天有什么想法" | 查看今天的想法 | `think ls --today` |
| "我有想过 xxx 吗" | 搜索想法 | `think search "xxx"` |
| "回顾一下" | 回顾想法 | `think review --week` |
| "我有多少想法" | 统计 | `think stats` |

---

## 4. 数据结构

### 文件位置

```
~/.think/think.db
```

### 表结构

```sql
CREATE TABLE ideas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,              -- 想法内容
    tags TEXT,                          -- 标签（JSON 数组）
    priority TEXT DEFAULT 'normal',     -- 优先级：low/normal/high
    status TEXT DEFAULT 'idea',         -- 状态：idea/todo/doing/done
    context TEXT,                       -- 上下文（在哪里产生的）
    source_agent TEXT,                  -- 来自哪个智能体
    note TEXT,                          -- 备注（展开内容）
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- 索引
CREATE INDEX idx_ideas_created_at ON ideas(created_at DESC);
CREATE INDEX idx_ideas_tags ON ideas(tags);
CREATE INDEX idx_ideas_status ON ideas(status);
CREATE INDEX idx_ideas_priority ON ideas(priority);
```

### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| content | TEXT | 想法内容（必需） |
| tags | TEXT | 标签，JSON 数组 `["agenthub", "decentralized"]` |
| priority | TEXT | 优先级：low/normal/high |
| status | TEXT | 状态：idea/todo/doing/done |
| context | TEXT | 上下文，如 "和阅咚咚讨论 Agent Hub" |
| source_agent | TEXT | 来源智能体，如 "yue" |
| note | TEXT | 展开内容，详细说明 |

---

## 5. 项目结构

```
ThinkDongDong/
├── src/think/                  # CLI 源码
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py                   # 入口
│   ├── const.py                 # 常量
│   │
│   ├── core/                    # 核心库
│   │   ├── __init__.py
│   │   ├── client.py            # Python SDK
│   │   └── models.py            # 数据模型
│   │
│   ├── commands/                # CLI 命令
│   │   ├── __init__.py
│   │   ├── add.py
│   │   ├── delete.py
│   │   ├── get.py
│   │   ├── init.py
│   │   ├── ls.py
│   │   ├── review.py
│   │   ├── search.py
│   │   ├── stats.py
│   │   └── update.py
│   │
│   └── db/                      # 数据库
│       ├── __init__.py
│       ├── connection.py
│       ├── schema.py
│       └── utils.py
│
├── agent/                       # Agent workspace
│   ├── IDENTITY.md
│   ├── SOUL.md
│   ├── TOOLS.md
│   ├── USER.md
│   ├── OVERVIEW.md
│   ├── MEMORY.md.template
│   └── HEARTBEAT.md
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── integration/
│   └── unit/
│
├── docs/
│   └── API_REFERENCE.md
│
├── pyproject.toml
├── README.md
├── ARCHITECTURE.md
├── WHY.md
└── .gitignore
```

---

## 6. 技术栈

| 组件 | 选择 | 理由 |
|------|------|------|
| 语言 | Python 3.11+ | 与其他智能体一致 |
| CLI 框架 | Typer | 类型安全，与阅咚咚一致 |
| 数据库 | SQLite | 本地私有，简单可靠 |
| 输出格式 | JSON | Agent 友好 |

---

## 7. 开发计划

### Phase 1: CLI 核心（1周）

| 任务 | 优先级 |
|------|--------|
| 项目初始化 | P0 |
| 数据库 schema | P0 |
| init 命令 | P0 |
| add 命令 | P0 |
| ls 命令 | P0 |
| get 命令 | P0 |
| search 命令 | P0 |
| delete 命令 | P0 |

### Phase 2: CLI 增强（1周）

| 任务 | 优先级 |
|------|--------|
| update 命令 | P1 |
| review 命令 | P1 |
| stats 命令 | P1 |
| --json 输出 | P1 |
| 测试覆盖 | P1 |

### Phase 3: Agent（1周）

| 任务 | 优先级 |
|------|--------|
| IDENTITY.md | P1 |
| SOUL.md | P1 |
| TOOLS.md | P1 |
| Agent 集成测试 | P2 |

---

## 8. 智能体矩阵更新

```
┌─────────────────────────────────────────────────────┐
│                  咕咚的智能体矩阵                      │
├─────────────────┬───────────────────────────────────┤
│ 🐹 仓咚咚        │ 💰 管钱（财务）                    │
├─────────────────┼───────────────────────────────────┤
│ 📚 阅咚咚        │ 📖 管知识（阅读摘录）              │
├─────────────────┼───────────────────────────────────┤
│ 💡 思咚咚        │ 🧠 管想法（灵感思考）              │
├─────────────────┼───────────────────────────────────┤
│ 📝 inBox        │ 📄 管笔记（待做 CLI）              │
├─────────────────┼───────────────────────────────────┤
│ 💬 小黑马        │ 🎯 总管                           │
└─────────────────┴───────────────────────────────────┘
```

---

## 9. 命名

- **中文名**：思咚咚
- **英文 ID**：think
- **CLI 包名**：think-cli
- **CLI 命令**：think
- **数据目录**：~/.think/
- **Emoji**：💡

---

*设计方案 v1 - 2026-03-15*
