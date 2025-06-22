from langchain.tools import tool
from ..utils import get_text

@tool
def markdown_tool(path: str) -> str:
    """ markdown 相关的处理工具
        Args:
            path: 传递的文件路径
    """
    
    return get_text(path=path)