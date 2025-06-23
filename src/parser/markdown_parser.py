from .base_parser import BaseParser
from ..tools import markdown_tool
from ..decorator import proxy_parser

"""
这是 markdown 解析器

Author:
    lvdaxianer
"""
class MarkdownParser(BaseParser):
    @proxy_parser
    def parser(self) -> str:
        """
        markdown 解析器

        Author:
            lvdaxianer

        Returns:
            返回 Markdown 内容
        """
        return markdown_tool.invoke({"path": self.file_path})