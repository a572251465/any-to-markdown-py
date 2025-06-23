from typing import Dict, Any
from ..models import ParserTypeModel
from .markdown_parser import MarkdownParser
from .base_parser import BaseParser
from pathlib import Path
from langchain.tools import tool

## 文件映射解析器
file_mapping_parser: Dict[ParserTypeModel, BaseParser] = {
    ParserTypeModel.md: MarkdownParser
}

@tool
def discover_parser(file_path: str) -> Any:
    """
    根据文件路径，识别出文件解析器，从而解析出 pdf 或是 markdown 或是 word中的内容
    返回文件中的内容

    Author:
        lvdaxianer

    Args:
        file_path 文件路径

    Returns:
        文件内容
    """

    ## 文件后缀
    file_suffix = Path(file_path).suffix.lstrip(".")

    ## 通过 code 拿到枚举值
    status = ParserTypeModel.from_value(file_suffix)

    ## 拿到解析器
    current_parser = file_mapping_parser[status]

    ## 执行解析器
    current_parser_instance = current_parser(file_path=file_path)
    text = current_parser_instance.parser()
    return text