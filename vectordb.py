import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader,PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

DATA_PATH = "data"
DB_PATH = "vector_db"

#CREATE DATABASE FUNCTION
def create_vector_db():
    print(f"---[1/4] Loading documents from {DATA_PATH}---")
    if not os.path.exists(DATA_PATH):
        os.mkdir(DATA_PATH)
        print("Created {DATA_PATH} folder. Please add some files there!")
        return
    
    #LOAD DOCUMENTS FROM .TXT FILES
    txt_loader= DirectoryLoader(DATA_PATH, glob="*txt", loader_cls= TextLoader)
    txt_documents = txt_loader.load()

    #LOAD DOCUMENTS FROM .PDF FILES
    pdf_loader = DirectoryLoader(DATA_PATH, glob="*.pdf", loader_cls=PyPDFLoader)
    pdf_docs = pdf_loader.load()

    documents = txt_documents + pdf_docs

    if not documents:
        print(f"No documents found in {DATA_PATH}. Please add some files there!")
        return
    print(f"Loaded {len(documents)} documents.")

    #CHUNK THE TEXT
    print("---[2/4] Splitting documents into chunks---")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)
    print(f"Split into {len(chunks)} chunks.")

    #CREATE EMBEDDINGS
    print("---[3/4] Creating embeddings using HuggingFace---")
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    print("---[4/4] Creating vector database---")
    db = Chroma.from_documents(documents=chunks, embedding= embedding_model, persist_directory=DB_PATH)
    print(f"Vector database created at {DB_PATH}")
# This ensures that code only runs when the script is executed directly and not when it is called through an import.
if __name__ == "__main__":
        create_vector_db()