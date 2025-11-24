import os
from langchain_openai import ChatOpenAI
from config.config import OPENROUTER_API_KEY, OPENROUTER_BASE_URL

def get_openrouter_model():
    """Initialize OpenRouter LLM"""
    try:
        model = ChatOpenAI(
            api_key=OPENROUTER_API_KEY,
            model="meta-llama/llama-3.1-70b-instruct",
            base_url=OPENROUTER_BASE_URL,
        )
        return model
    except Exception as e:
        raise RuntimeError(f"Error initializing OpenRouter model: {e}")
