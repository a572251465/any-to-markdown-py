from typing import List, Tuple, TypedDict, Any

"""这里定义了 Agent 状态
    Author: lvdaxianer
"""
class AgentState(TypedDict):
    file_path: str
    output: Any
    history: List[Tuple[str, str]]  # (action, result)