"""常量定义"""

VERSION = "0.1.0"
APP_NAME = "思咚咚"

# 数据目录 - 统一放在 ~/.dong/ 下
from pathlib import Path
DATA_DIR = Path.home() / ".dong" / "think"
DB_PATH = DATA_DIR / "think.db"

# 默认值
DEFAULT_LIMIT = 20

# 优先级
PRIORITY_LOW = "low"
PRIORITY_NORMAL = "normal"
PRIORITY_HIGH = "high"
PRIORITIES = [PRIORITY_LOW, PRIORITY_NORMAL, PRIORITY_HIGH]

# 状态
STATUS_IDEA = "idea"
STATUS_TODO = "todo"
STATUS_DOING = "doing"
STATUS_DONE = "done"
STATUSES = [STATUS_IDEA, STATUS_TODO, STATUS_DOING, STATUS_DONE]
