import torch
torch.classes.__path__ = []
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
import streamlit as st
import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

load_dotenv()

# -------------------- Streamlit UI --------------------
# To give a nice interface to the chatbot
st.set_page_config(page_title="Policy-RAG-BOT", page_icon="📚")
st.title(" Ask for Economic Survey 2024-2025 and Policies information 📚")


# -------------------- LLM Factory --------------------
# Returns an LLM based on the LLM_PROVIDER environment variable
def get_llm():
    provider = os.getenv("LLM_PROVIDER", "groq").lower()

    if provider == "openai":
        return ChatOpenAI(
    openai_api_base="https://openrouter.ai/api/v1",
    model_name="mistralai/devstral-2512:free"
)

    if provider == "huggingface":
        llm = HuggingFaceEndpoint(
            repo_id ="Qwen/Qwen3-4B-Instruct-2507",
            task="text-generation",
            max_new_tokens=512,
            do_sample=False,
        )
        return ChatHuggingFace(llm=llm)

    else:
        return ChatGroq(model="llama-3.1-8b-instant", temperature=0)


# -------------------- RAG Chain --------------------
@st.cache_resource
def get_qa_chain():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = Chroma(
        persist_directory="vector_db",
        embedding_function=embeddings,
    )

    retriever = vectorstore.as_retriever(search_kwargs={"k": 1})
    llm = get_llm()

    prompt = ChatPromptTemplate.from_template(
        """
You are a helpful assistant well versed in government policies especially on Environment policy and schemes. 
In response to the user's question, You HAVE to be polite and answer the user's question using ONLY the context below.
Give your answer in simple and plain language explaining it in detail. If the answer is not in the context, do not give wrong answer 
but politely refuse by responding "I am not an expert in that."

<context>
{context}
</context>

Question: {input}
"""
    )

    # LCEL-style RAG chain
    rag_chain = (
        {
            "context": retriever,
            "input": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain
qa_chain = get_qa_chain()
# while True:
#     user_input= input("\n You:")
#     if user_input.lower() =="quit":
#         break

#     print("AI:", end=" ")
#     print(qa_chain.invoke(user_input))

user_input = st.chat_input("Ask a question about Environment Policy or type 'quit' to exit:")
if user_input:
    # 1. Handle Exit first
    if user_input.lower() == "quit":
        st.info("Exiting...")
        st.stop()

    # 2. Display User Message
    with st.chat_message("user"):
        st.markdown(user_input)

    # 3. Process Assistant Response
    with st.chat_message("assistant"):
        with st.spinner("Searching documents..."):
            try:
    
                output = qa_chain.invoke(user_input)

                st.markdown(output)
            except Exception as e:
                st.error("--- REAL ERROR FOUND ---")
                st.exception(e)  # This will show a big red/black box with the full logic path
                print(f"Terminal Error: {e}") # Check your VS Code terminal for this too
                st.error(f"Error: {e}")