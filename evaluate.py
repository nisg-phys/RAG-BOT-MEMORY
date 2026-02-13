

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from config import VECTOR_DB_DIR, EMBEDDING_MODEL, RETRIEVAL_K

# Test questions
TEST_QUERIES = [
    "What environmental schemes were introduced in 2024?",
    "What is mentioned about forest conservation?",
    "What climate initiatives were launched?",
]

def evaluate_retrieval():

    print("Loading vector database...")

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

    vectordb = Chroma(
        persist_directory=VECTOR_DB_DIR,
        embedding_function=embeddings
    )

    retriever = vectordb.as_retriever(
        search_kwargs= RETRIEVAL_K
    )

    print("\nEvaluating retrieval quality\n")

    for query in TEST_QUERIES:

        docs = retriever.invoke(query)

        print("="*50)
        print("Query:", query)
        print("Retrieved chunks:", len(docs))

        if docs:
            print("Top chunk preview:")
            print(docs[0].page_content[:200])
        else:
            print("No chunks retrieved")

        print("="*50)


if __name__ == "__main__":
    evaluate_retrieval()
