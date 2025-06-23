from langchain_deepseek import ChatDeepSeek
from langchain_openai import ChatOpenAI
from langchain_core.language_models.chat_models import BaseChatModel
from typing import Union
from ..models import EnvEnumModel
import os

"""
通过环境变量中内容 拿到聊天的Chat

Author:
    lvdaxianer

Returns:
    返回 BaseChatModel || None
"""
def get_chat() -> Union[BaseChatModel, None]:
    deepseek_model_name = os.getenv(EnvEnumModel.deepseek_model_name.value, "deepseek_model_name")
    deepseek_api_key = os.getenv(EnvEnumModel.deepseek_api_key.value, "")
    deepseek_api_base = os.getenv(EnvEnumModel.deepseek_api_base.value, "https://api.deepseek.com/v1")

    ## 这里 优先选择 deepseek
    if not deepseek_model_name:
        return ChatDeepSeek(
            model=deepseek_model_name,
            base_url=deepseek_api_base,
            api_key=deepseek_api_key
        )

    return None