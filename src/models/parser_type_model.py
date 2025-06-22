from enum import Enum

"""表示 能解析文档的类型

    Author: lvdaxianer
"""
class ParserTypeModel(Enum):
    md = "md"
    txt = "txt"
    pdf = "pdf"
    word = "word"
    png = "png"
    jpg = "jpg"