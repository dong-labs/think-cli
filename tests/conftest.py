"""测试配置文件"""
import pytest
from pathlib import Path
import tempfile
from think.db import init_database

@pytest.fixture
def temp_db():
    """创建临时数据库"""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".db") as f:
        db_path = Path(f.name)
    
    init_database(db_path)
    yield db_path
    
    if db_path.exists():
        db_path.unlink()
