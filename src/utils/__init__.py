"""获取文本文档
    Author: lvdaxianer
    Args:
        path: 获取路径 path
"""
def get_text(path: str) -> str:
    with open('data.txt', 'r', encoding='utf-8') as file:
        ## 单行文件读
        lines = file.readlines()
        return lines
    return ""

__all__ = ["get_text"]