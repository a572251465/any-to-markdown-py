from fastapi import APIRouter
from ..models import ResponseModel
from pydantic import BaseModel

## body 请求体
class PathModel(BaseModel):
    path: str

## 这里 构建单个实例
router = APIRouter(prefix="/convert")

"""通过 path路径 转换为markdown

    Author:
        lvdaxianer
    Args:
        item 传递的body, 其中包括文件路径
"""
@router.post("/byPath")
async def convert_markdown_by_path(item: PathModel) -> 'ResponseModel':
    return ResponseModel.ok(data="")