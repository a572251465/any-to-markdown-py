from enum import Enum

"""
表示 能解析文档的类型

Author:
    lvdaxianer
"""
class ParserTypeModel(Enum):
    md = "md"
    txt = "txt"
    pdf = "pdf"
    word = "word"
    png = "png"
    jpg = "jpg"

    """
    通过字符串 code 转换为 枚举类型

    Author:
        lvdaxianer
    
    Args:
        value: 具体的 value 的值
    """
    @classmethod
    def from_value(cls, value: str) -> "ParserTypeModel":
        for status in cls:
            if status.value == value:
                return status
        raise ValueError(f"Invalid status: {value}")