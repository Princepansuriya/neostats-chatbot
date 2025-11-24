import streamlit as st
from models.llm import get_openrouter_model
from utils.rag_utils import create_vector_store, retrieve_answer
from utils.search_utils import web_search

# --- FIX: Simple response mode handler ---
def apply_response_mode(mode, text):
    if mode == "Concise":
        return text[:400] + "..." if len(text) > 400 else text
    elif mode == "Detailed":
        return text + "\n\n(Answered in detailed mode)"
    else:
        return text

# --------------------------------------------------

st.set_page_config(page_title="OpenRouter RAG Chatbot", layout="wide")

@st.cache_resource
def load_vectorstore():
    return create_vector_store()

vector_store = load_vectorstore()
llm = get_openrouter_model()

st.sidebar.title("⚙ Settings")
mode = st.sidebar.radio("Response Mode", ["Concise", "Detailed"])
use_web = st.sidebar.checkbox("Enable Live Web Search")
use_rag = st.sidebar.checkbox("Enable RAG Document Search")

st.title("🤖 AI Chatbot (OpenRouter + RAG + Web Search)")

if "history" not in st.session_state:
    st.session_state.history = []

# Display history
for msg in st.session_state.history:
    st.chat_message(msg["role"]).markdown(msg["content"])

query = st.chat_input("Ask something...")

if query:
    st.chat_message("user").markdown(query)
    st.session_state.history.append({"role": "user", "content": query})

    final_context = ""

    # RAG Search
    if use_rag:
        rag_context = retrieve_answer(query, vector_store)
        final_context += f"RAG Context:\n{rag_context}\n\n"

    # Web Search (Tavily)
    if use_web:
        search_info = web_search(query)
        final_context += f"Web Search Info:\n{search_info}\n\n"

    prompt = f"""
    You are an intelligent assistant. Use the context below if helpful.

    {final_context}

    User Question: {query}
    """

    response = llm.invoke(prompt).content
    response = apply_response_mode(mode, response)

    st.chat_message("assistant").markdown(response)
    st.session_state.history.append({"role": "assistant", "content": response})
