
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
from config import VECTOR_DB_DIR, RETRIEVAL_K

load_dotenv()

# -------------------- Streamlit UI --------------------
# To give a nice interface to the chatbot
st.set_page_config(page_title="Policy-RAG-BOT", page_icon="📚")
st.title(" Have Questions about Environment Policy implementation of 2024?📚")


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
        persist_directory=VECTOR_DB_DIR,
        embedding_function=embeddings,
    )

    retriever = vectorstore.as_retriever(search_kwargs=RETRIEVAL_K)
    llm = get_llm()

    prompt = ChatPromptTemplate.from_template(
        """
You are a helpful assistant well versed in government policies especially on Environment policy and schemes. 
In response to the user's question, You HAVE to be polite and answer the user's question using ONLY the context below.
Give your answer in simple and plain language explaining it in detail. If the answer is not in the context, do not give wrong answer 
but politely refuse by responding "I am not an expert in that". You do not have to give an answer to a user's question 
without context at all. What you SHOULD do is, in addition to "I am not an expert in that", mention some additional fact
from the context that they might be interested in knowing?

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


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Ask a question about Environment Policy Achievements of 2024")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)

    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("assistant"):
        with st.spinner("Searching knowledge base..."):
            try:
                answer = qa_chain.invoke(user_input)
                st.markdown(answer)

                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )

            except Exception as e:
                st.error(f"Error: {e}")
