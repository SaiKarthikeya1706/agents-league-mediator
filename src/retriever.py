from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

class HybridRetriever:
    def __init__(self, documents, collection_name="local_docs"):
        # We use Gemini's embedding model
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        
        # Create a persistent vector store
        self.vectorstore = Chroma.from_documents(
            documents, 
            self.embeddings,
            collection_name=collection_name,
            persist_directory="./data/vector_db"
        )
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 5})

    def search(self, query, top_n=5):
        # Update retriever configuration dynamically
        self.retriever.search_kwargs["k"] = top_n
        results = self.retriever.invoke(query)
        
        # Clean up the output to make it easier for the LLM to read
        return [{"text": doc.page_content, "source": doc.metadata.get("source", "unknown")} for doc in results]

    def close(self):
        # Properly close the database connection
        self.vectorstore = None