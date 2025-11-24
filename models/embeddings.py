from langchain_openai import OpenAIEmbeddings
from config.config import OPENROUTER_API_KEY, OPENROUTER_BASE_URL

def get_embedding_model():
    """Return embedding model compatible with vector stores."""
    return OpenAIEmbeddings(
        api_key=OPENROUTER_API_KEY,
        base_url=OPENROUTER_BASE_URL,
        model="text-embedding-3-large"
    )
