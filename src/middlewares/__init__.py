from .log_requests import binding_log_requests
from fastapi import FastAPI

"""构建 logging 的方法

    Author: lvdaxianer
    Args:
        app: FastAPI 的实例
"""
def binding_logging_funs(app: FastAPI):
    for fn in [binding_log_requests]:
        fn(app=app)

__all__ = ["binding_logging_funs"]
