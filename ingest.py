import os
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

# Load environment variables
load_dotenv()

# Constants
DATA_PATH = "data/"
FAISS_PATH = "faiss_index"

def create_vectorstore():
    """
    Create a FAISS vector store from documents in the data directory.
    """
    print("Loading documents...")
    
    documents = []
    
    # Load PDF files
    pdf_loader = DirectoryLoader(
        DATA_PATH,
        glob="**/*.pdf",
        loader_cls=PyPDFLoader,
        show_progress=True
    )
    pdf_docs = pdf_loader.load()
    documents.extend(pdf_docs)
    
    # Load TXT files
    txt_loader = DirectoryLoader(
        DATA_PATH,
        glob="**/*.txt",
        loader_cls=TextLoader,
        show_progress=True
    )
    txt_docs = txt_loader.load()
    documents.extend(txt_docs)
    
    if not documents:
        print("No documents found in the data directory. Please add some .pdf or .txt files to the 'data/' folder.")
        return
    
    print(f"Loaded {len(documents)} documents")
    print("Splitting documents...")
    
    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    
    docs = text_splitter.split_documents(documents)
    print(f"Split into {len(docs)} chunks")
    
    print("Creating embeddings and FAISS index...")
    
    # Initialize OpenAI embeddings
    embeddings = OpenAIEmbeddings()
    
    # Create FAISS vector store from documents
    db = FAISS.from_documents(docs, embeddings)
    
    # Save the index to disk
    db.save_local(FAISS_PATH)
    
    print(f"Ingestion complete! FAISS index saved to '{FAISS_PATH}' directory.")
    print(f"You can now run the Streamlit app with: streamlit run app.py")

if __name__ == "__main__":
    create_vectorstore()