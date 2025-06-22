from fastapi import FastAPI, Request, Response
from loguru import logger

"""构建请求日志

    Author: lvdaxianer
    Args:
        app: FastAPI 请求实例
"""
def binding_log_requests(app: FastAPI):

    """请求日志的函数

        Author: lvdaxianer
        Args:
            request: 这是请求实例
            call_next: 要执行下一个函数 
    """
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        # 记录请求信息
        logger.info(f"Request: {request.method} {request.url}")
        logger.debug(f"Headers: {request.headers}")
        logger.debug(f"Query Params: {request.query_params}")
        logger.debug(f"Path Params: {request.path_params}")
        
        # 对于需要记录 body 的情况
        if await request.body():
            logger.debug(f"Request Body: {await request.json()}")

        response = await call_next(request)
        
        # 记录响应信息（谨慎记录响应体，可能包含敏感信息）
        logger.info(f"Response Status: {response.status_code}")
        logger.debug(f"Response Headers: {response.headers}")
        
        return response