# TOOLS.md - 工具箱

我的核心工具是 `dong-think` CLI。

## 安装

```bash
pipx install dong-think
```

## 命令列表

### 初始化

```bash
dong-think init
```

### 记录想法

```bash
dong-think add "一个新想法"
dong-think add "三层架构设计" --tags "架构,设计"
dong-think add "重要想法" --priority high
```

### 列出想法

```bash
dong-think list              # 列出所有想法
dong-think list --limit 50   # 指定数量
dong-think list --tag "架构" # 按标签筛选
```

### 搜索想法

```bash
dong-think search "关键词"
dong-think search "架构" --limit 10
```

### 获取详情

```bash
dong-think get 123           # 获取想法详情
```

### 更新想法

```bash
dong-think update 123 --content "更新内容"
dong-think update 123 --priority high
```

### 删除想法

```bash
dong-think delete 123
```

### 查看标签

```bash
dong-think tags              # 列出所有标签及数量
```

### 统计信息

```bash
dong-think stats             # 统计想法数量、状态分布、标签分布
```

### 回顾想法

```bash
dong-think review            # 随机回顾一个想法
```

## JSON 输出

所有命令支持 JSON 输出，方便 AI 解析：

```bash
dong-think add "xxx"
dong-think list
dong-think search "关键词"
dong-think stats
```

## 数据库

数据存储在 `~/.dong/think.db`

---

*💡 灵感稍纵即逝，记录永恒*
