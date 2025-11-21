from typing import TypedDict, Annotated, List
from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages
from typing import Optional

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    user_query: str
    decision: str
    reply: str

    session_id: Optional[str]