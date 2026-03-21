# 思咚咚

> 💡 记录灵感和思考的 CLI 工具

[![Version](https://img.shields.io/badge/Version-0.6.0-blue.svg)](https://pypi.org/project/dong-think/)

## 安装

```bash
pipx install dong-think
```

## 快速开始

```bash
# 初始化
dong-think init

# 记录想法
dong-think add "Agent Hub 可以去中心化"
dong-think add "想法：用 IPFS 存 Agent 包" --tag ipfs

# 列出想法
dong-think list
dong-think list --today
dong-think list --tag agenthub

# 搜索
dong-think search "去中心化"

# 回顾
dong-think review --week

# 统计
dong-think stats
```

## 命令

| 命令 | 说明 |
|------|------|
| `dong-think init` | 初始化数据库 |
| `dong-think add` | 记录想法 |
| `dong-think list` | 列出想法 |
| `dong-think get` | 获取详情 |
| `dong-think search` | 搜索想法 |
| `dong-think update` | 更新想法 |
| `dong-think delete` | 删除想法 |
| `dong-think review` | 回顾想法 |
| `dong-think stats` | 统计信息 |

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
