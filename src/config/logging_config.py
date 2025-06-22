from loguru import logger
import sys

"""表示 添加 logging config 配置

    Author:
        lvdaxianer
"""
def add_logging_config():
    format = "{time} {name} {level} {message}"
    level = "DEBUG"

    ## 这里文件输出
    logger.add("logs/info_{time:YYYY-MM}.log", format=format, level=level, rotation="5 mb", backtrace=True, diagnose=True)
    ## 这里是控制台打印
    logger.add(sys.stdout, format=format, level=level, backtrace=True, diagnose=True)
    ## 错误日志单独打印
    logger.add("logs/error_{time:YYYY-MM}.log", level="ERROR",rotation="5 mb",format=format, backtrace=True, diagnose=True)

## 测试 case
if __name__ == "__main__":
    add_logging_config()
    logger.info("~~~~~")