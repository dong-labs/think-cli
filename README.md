# 思咚咚

> 💡 记录灵感和思考的 CLI 工具

## 安装

```bash
pip install think-cli
```

## 快速开始

```bash
# 初始化
think init

# 记录想法
think add "Agent Hub 可以去中心化"
think add "想法：用 IPFS 存 Agent 包" --tag ipfs

# 列出想法
think list
think list --today
think list --tag agenthub

# 搜索
think search "去中心化"

# 回顾
think review --week

# 统计
think stats
```

## 命令

| 命令 | 说明 |
|------|------|
| `think init` | 初始化数据库 |
| `think add` | 记录想法 |
| `think list` | 列出想法 |
| `think get` | 获取详情 |
| `think search` | 搜索想法 |
| `think update` | 更新想法 |
| `think delete` | 删除想法 |
| `think review` | 回顾想法 |
| `think stats` | 统计信息 |

## 数据存储

```
~/.think/think.db
```

## 开发

```bash
# 克隆
git clone https://github.com/gudong/think-cli.git
cd think-cli

# 安装依赖
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"

# 运行测试
pytest
```

## License

MIT
