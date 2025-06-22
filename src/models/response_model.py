from dataclasses import dataclass
from typing import Any

"""响应的返回值类

    Author:
        lvdaxianer
"""
@dataclass
class ResponseModel:
    code: int
    message: str
    status: bool
    data: Any

    @staticmethod
    def ok(data: Any) -> 'ResponseModel':
        return ResponseModel(code=200, status=True, data=data, message="")