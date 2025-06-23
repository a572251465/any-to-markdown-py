from langchain.agents import AgentExecutor
from langchain_core.runnables import RunnableLambda 

def exec_tool(input: str) -> str:
    print(f"input: {input}")
    return input

agent = AgentExecutor(
    agent= {"input": lambda x: x["input"]} | RunnableLambda(exec_tool),
    tools=[],
    return_intermediate_steps=True
)
agent.invoke({"input": "~~~~"})