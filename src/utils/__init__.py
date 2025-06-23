import os

"""获取文本文档
    Author: lvdaxianer
    Args:
        path: 获取路径 path
"""
def get_text(path: str) -> str:
    with open(path, 'r', encoding='utf-8') as file:
        ## 单行文件读
        lines = file.readlines()
        return lines
    return ""

"""
是否 debug

Author:
    lvdaxianer

Returns:
    bool True or False, default is False
"""
def is_debug() -> bool:
    return  os.getenv("debug", "True") == "True" 

__all__ = ["get_text", "is_debug"]