from langchain_openai import ChatOpenAI
from app.core.config import settings

def get_llm(temperature: float = 0, model_name: str = None):
    if not settings.OPENAI_API_KEY:
        raise ValueError("OpenAI API key is not set in the configuration.")

    model = model_name if model_name else settings.LLM_MODEL

    return ChatOpenAI(
        openai_api_key=settings.OPENAI_API_KEY,
        model_name=model,
        temperature=temperature
    )