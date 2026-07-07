import os
import sys
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

load_dotenv()

# Resolve project root (parent of src/) regardless of current working directory
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POLICY_PATH = os.path.join(ROOT_DIR, "data", "policy.txt")
CHROMA_DIR = os.path.join(ROOT_DIR, "chroma_db")

def main():
    if not os.path.exists(POLICY_PATH):
        print(f"Could not find {POLICY_PATH}")
        sys.exit(1)

    with open(POLICY_PATH, "r") as f:
        policy_text = f.read()

    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = splitter.split_text(policy_text)

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=os.environ["GOOGLE_API_KEY"]
    )

    vectorstore = Chroma.from_texts(chunks, embeddings, persist_directory=CHROMA_DIR)
    print(f"Indexed {len(chunks)} policy chunks into {CHROMA_DIR}")

if __name__ == "__main__":
    main()