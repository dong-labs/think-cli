# TOOLS.md - 工具箱

我的核心工具是 `think` CLI。

## 命令列表

### 记录想法

```bash
think add "想法内容"
think add "想法内容" --tag 标签
think add "想法内容" --priority high
```

### 列出想法

```bash
think list              # 列出最近 20 条
think list --today      # 今天的想法
think list --week       # 本周的想法
think list --tag xxx    # 按标签筛选
```

### 搜索想法

```bash
think search "关键词"
```

### 获取详情

```bash
think get 123           # 获取 ID 为 123 的想法详情
```

### 更新想法

```bash
think update 123 --status todo
think update 123 --add-tag 重要
think update 123 --priority high
```

### 删除想法

```bash
think delete 123 --force
```

### 回顾想法

```bash
think review            # 随机一条
think review --today    # 今天的想法
think review --week     # 本周的想法
```

### 统计信息

```bash
think stats
```

## JSON 输出

所有命令支持 `--json` 参数，方便解析：

```bash
think add "xxx" --json
think list --json
think search "xxx" --json
```

---

*💡 工具在手，想法我有*
