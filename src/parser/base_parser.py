from pydantic import BaseModel
from abc import ABC, abstractmethod

"""
这是 基础解析器

Author:
    lvdaxianer
"""
class BaseParser(BaseModel, ABC):
    file_path: str

    """
    待 实现的抽象方法
            
    Author:
        lvdaxianer
    """
    @abstractmethod
    def parser(self) -> str:
        pass