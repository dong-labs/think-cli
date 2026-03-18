# OVERVIEW.md - 项目概览

## 项目信息

| 项目 | 值 |
|------|-----|
| 中文名 | 思咚咚 |
| 英文 ID | think |
| CLI 命令 | think |
| 数据目录 | ~/.think/ |
| 项目目录 | repos/ThinkDongDong/ |

## 核心功能

| 功能 | 命令 |
|------|------|
| 初始化 | think init |
| 记录 | think add |
| 列出 | think list |
| 搜索 | think search |
| 回顾 | think review |
| 统计 | think stats |

## 数据结构

```sql
ideas (
    id, content, tags, priority, status,
    context, source_agent, note,
    created_at, updated_at
)
```

## 开发状态

- [x] CLI 核心
- [x] Agent workspace
- [ ] 测试覆盖
- [ ] PyPI 发布

---

*💡 让你的思考有迹可循*
