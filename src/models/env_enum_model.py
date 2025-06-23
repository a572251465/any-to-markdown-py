from enum import Enum

"""
定义环境变量的枚举

Author:
    lvdaxianer
"""

class EnvEnumModel(Enum):
    web_service_host = "web_service_host"
    web_service_port = "web_service_port"
    root_prefix = "root_prefix"

    ## deepseek options
    deepseek_model_name = "deepseek_model_name"
    deepseek_api_key = "deepseek_api_key"
    deepseek_api_base = "https://api.deepseek.com/v1"