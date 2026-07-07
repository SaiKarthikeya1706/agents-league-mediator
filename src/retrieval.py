import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter

_embeddings = None
_static_store = None

def get_embeddings():
    global _embeddings
    if _embeddings is None:
        _embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
            google_api_key=os.environ["GOOGLE_API_KEY"]
        )
    return _embeddings

def get_static_store():
    global _static_store
    if _static_store is None:
        _static_store = Chroma(persist_directory="chroma_db", embedding_function=get_embeddings())
    return _static_store

def build_ephemeral_store(raw_text: str):
    if not raw_text or not raw_text.strip():
        return None
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = splitter.split_text(raw_text)
    if not chunks:
        return None
    return Chroma.from_texts(chunks, get_embeddings())

def retrieve_context(query: str, uploaded_text: str = "", k: int = 4) -> str:
    parts = []

    static_hits = get_static_store().similarity_search(query, k=k)
    if static_hits:
        parts.append("--- RELEVANT SYSTEM POLICY ---")
        parts.extend(doc.page_content for doc in static_hits)

    ephemeral = build_ephemeral_store(uploaded_text)
    if ephemeral:
        upload_hits = ephemeral.similarity_search(query, k=k)
        parts.append("--- RELEVANT USER-UPLOADED CONTENT (prioritize this) ---")
        parts.extend(doc.page_content for doc in upload_hits)

    return "\n\n".join(parts) if parts else "No relevant context found."