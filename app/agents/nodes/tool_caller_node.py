from langchain_core.messages import HumanMessage, AIMessage
from app.agents.agent_state import AgentState
from app.agents.tools.sql_query_tool import sql_query_tool
import traceback

from app.core.logger import logger


def tool_caller_node(state: AgentState) -> AgentState:
    try:
        decision = state.get("reply", "").strip().lower()
        messages = state.get("messages", [])
        session_id = state.get("session_id", None)


        if decision == "database_query_tool":
            logger.info("tool_caller_node: Routing to sql_query_tool.")


            tool_input = {
                "user_query": messages,
                "session_id": session_id
            }

            result = sql_query_tool.invoke(tool_input)
            state["reply"] = result
        else:
            logger.warning(f"tool_caller_node: Unknown decision '{decision}'.")
            state["reply"] = "I'm sorry, I seem to be confused. Can you rephrase that, please? 🥺"

    except Exception as e:
        logger.error(f"Error in tool_caller_node: {e}\n{traceback.format_exc()}")
        state[
            "reply"] = f"Oops! I hit a snag while trying to find that information. Please try again or ask a simple question. (Error: {str(e)[:50]}...)"

    return state