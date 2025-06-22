from .convert import router as convert_router
from fastapi import FastAPI

"""这是挂载路由的方法

    Author: lvdaxianer

    Args:
        app: FastAPI 实例
"""
def mount_routes(app: FastAPI):
    app.include_router(convert_router)

__all__ = ["mount_routes"]