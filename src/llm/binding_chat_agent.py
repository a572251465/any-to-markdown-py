from .get_chat import get_chat
from langchain.agents import Agent
from langchain_core.runnables import Runnable, RunnableLambda
from typing import Union
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import AgentOutputParser

"""
构建 llm agent

Author:
    lvdaxianer

Returns:
    返回执行的 Agent or Runnable
"""
def binding_chat_agent() -> Union[Agent, Runnable]:
    ## 拿到聊天信息
    chat = get_chat()
    if not chat:
        return RunnableLambda(lambda x : x["input"])

    ## 系统消息
    system_message = """
    你是一个经验丰富的文档总结助手，你的任务是将 提供的内容转换为 语义丰富的markdown内容。要求如下:
    1. markdown 表示内容不能有任何差别，一个字不能多，一个字不能少
    2. 但是, markdown的标题, 可以根据内容进行总结
    3. 最后只需要返回 转换后的markdown内容 即可。
    """

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_message),
            ("user", "{input}")
        ]
    )

    return prompt | chat | AgentOutputParser