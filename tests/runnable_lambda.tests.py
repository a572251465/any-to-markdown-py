from langchain_core.runnables import RunnableLambda

runnable = RunnableLambda(lambda x: x["input"])
print(runnable.invoke({"input": "~~~"}))