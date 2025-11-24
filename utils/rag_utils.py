import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader, TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

DATA_FOLDER = "data"  # can be: folder OR single file


def load_documents():
    # If 'data' path does NOT exist → no RAG
    if not os.path.exists(DATA_FOLDER):
        print("No data path found → RAG disabled.")
        return []

    # If 'data' is a FILE (PDF or text) → load directly
    if os.path.isfile(DATA_FOLDER):
        print("Loading single file for RAG...")
        # Auto-detect loader
        if DATA_FOLDER.lower().endswith(".pdf"):
            return PyPDFLoader(DATA_FOLDER).load()
        else:
            return TextLoader(DATA_FOLDER).load()

    # If 'data' is a DIRECTORY → load all PDF files
    print("Loading folder documents for RAG...")
    loader = DirectoryLoader(
        DATA_FOLDER,
        glob="**/*.pdf",
        loader_cls=PyPDFLoader
    )
    
    docs = loader.load()
    return docs


def create_vector_store():
    docs = load_documents()

    if len(docs) == 0:
        print("No documents found → RAG disabled.")
        return None

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = splitter.split_documents(docs)

    embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")
    vector_store = FAISS.from_documents(chunks, embedding_model)

    return vector_store


def retrieve_answer(query, vector_store):
    if vector_store is None:
        return "No RAG documents found."

    docs = vector_store.similarity_search(query, k=3)
    return "\n\n".join([d.page_content for d in docs])
