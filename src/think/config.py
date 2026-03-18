"""配置管理模块

继承 dong.config.Config，管理 think-cli 的用户配置。
"""

from dong.config import Config


class ThinkConfig(Config):
    """思咚咚配置类"""

    @classmethod
    def get_name(cls) -> str:
        return "think"

    @classmethod
    def get_defaults(cls) -> dict:
        return {
            "default_tags": ["idea", "insight"],
            "default_limit": 20,
        }


# 便捷函数
def get_config() -> dict:
    return ThinkConfig.load()

def get_default_tags() -> list:
    return ThinkConfig.get("default_tags", ["idea", "insight"])

def get_default_limit() -> int:
    return ThinkConfig.get("default_limit", 20)
