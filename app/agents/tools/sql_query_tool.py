from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.tools import tool
from sqlalchemy import text
import traceback
from typing import List, Dict, Any

from app.agents.llm_manager import get_llm
from app.agents.prompt.sql_generator_prompt import SQL_GENERATOR_PROMPT
from app.agents.prompt.sql_nl_responder_prompt import SQL_NL_RESPONDER_PROMPT
from app.core.logger import logger
from app.db.dbconnection import SessionLocal


@tool
def sql_query_tool(user_query: List[Dict[str, Any]], session_id: str) -> str:
    """
    Generate and Execute SQL query from user_query and context, including session_id.
    """
    messages = user_query

    user_query_content = messages[-1].get('content', '') if messages else ''

    logger.info(f"sql_query_tool received messages: {len(messages)}, Session ID: {session_id}")

    try:
        llm_sql_gen = get_llm(temperature=0)
        db_schema = get_db_info()
        formatted_prompt = SQL_GENERATOR_PROMPT.format(database_schema=db_schema)

        context_info = f"Current Session ID: {session_id}"

        gen_messages = [
            SystemMessage(content=formatted_prompt),
            HumanMessage(
                content=f"Context: {context_info}\nUser Query: {user_query_content}\nConversation History: {messages}")
        ]

        response = llm_sql_gen.invoke(gen_messages)
        sql_query = response.content.strip().replace("`", "").replace(";", "")

        logger.info(f"LLM Generated Query:\n{sql_query}")

        if not sql_query.lower().strip().startswith(("select", "insert", "update", "delete")):
            logger.warning(f"LLM did not generate a valid SQL query: {sql_query}")
            return "I need a clearer request to check the database. Could you rephrase your question about the cafe's data? 🍰"

    except Exception as e:
        logger.error(f"Error generating query: {e}\n{traceback.format_exc()}")
        return f"Oops! I couldn't form the right question for the database. ({str(e)[:30]}...)"

    session = SessionLocal()
    try:
        result = session.execute(text(sql_query))

        if sql_query.lower().startswith("select"):
            rows = result.fetchall()
            keys = result.keys()
            data = [dict(zip(keys, row)) for row in rows]

            system_message2 = SQL_NL_RESPONDER_PROMPT

            # Messages for the NL LLM
            messages2 = [
                SystemMessage(content=system_message2),
                HumanMessage(content=f"User Query: {user_query_content}\nSQL Result: {data}")
            ]

            llm_nl_gen = get_llm(temperature=0)
            response2 = llm_nl_gen.invoke(messages2)
            logger.info(f"Final bot response:\n{response2.content}")
            return response2.content

        else:  # INSERT, UPDATE, DELETE
            session.commit()
            logger.info("Successfully executed non-select query.")
            return "Thank you! I've successfully updated the information in our system. What's next? ✨"

    except Exception as e:
        session.rollback()
        logger.error(f"Error executing query: {e}\n{traceback.format_exc()}")
        return f"I'm sorry, I couldn't execute that command in the database. ({str(e)[:30]}...)"
    finally:
        session.close()