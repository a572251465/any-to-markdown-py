from functools import wraps
from loguru import logger
import json
from ..utils import is_debug

"""
解析器的代理类

Author:
    lvdaxianer

Args:
    funs 要代理的方法

Returns:
    返回包裹的函数
"""
def proxy_parser(func):
    @wraps(func)    
    def wrapper(*args, **kwargs):
        ## exec before
        logger.debug(f">>> call function name: {func.__name__}")
        logger.debug(f">>> call function params: {json.dumps(kwargs)}")

        ## exec function
        result = func(*args, **kwargs)

        ## exec after
        if is_debug():
            logger.debug(f">>> call function response: {result}")
        return result

    return wrapper