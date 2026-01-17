# Policy-RAG-BOT 📚

**Policy-RAG-BOT** is a Retrieval-Augmented Generation (RAG) based chatbot that allows users to query government policy documents through a simple conversational interface, instead of navigating complex official websites.

The project currently demonstrates this idea using the **Year-End Review 2024: Ministry of Environment, Forest and Climate Change (India)**, and is designed to be easily extensible to *any* government policy document (PDFs, reports, press releases, etc.).

---

## 🎯 Project Motivation

Government policy information is often:
- Scattered across multiple web pages
- Written in dense, formal language
- Hard to search for specific answers

This project shows how **modern LLM-based systems + vector search** can be used to build **transparent, document-grounded policy assistants** that:
- Answer only from official sources
- Refuse gracefully when information is missing
- Remain auditable and extensible

---

## 🧠 Key Features

- **Retrieval-Augmented Generation (RAG)** using LangChain
- **Strict grounding**: answers only from retrieved context
- **Graceful refusal** when information is not found
- **Conversation memory support** (chat history preserved)
- **Multi-LLM backend support**
  - Groq
  - OpenRouter (OpenAI-compatible)
  - Hugging Face
- **Pluggable document ingestion** (any PDF / policy document)
- **Streamlit-based UI** for nice interface while asking questions
---

## 🏗️ Architecture Overview

1. Policy documents are embedded using **Hugging Face sentence transformers**
2. Embeddings are stored in a **Chroma vector database**
3. User queries are:
   - Embedded
   - Retrieved against the vector store
   - Passed to an LLM with retrieved context
4. The LLM is instructed to:
   - Answer **only from context**
   - Refuse politely if context is insufficient
   - Suggest related information when refusing

This design ensures **faithful, non-hallucinatory answers**.

---

## 📦 Tech Stack

- **Language**: Python
- **Frameworks**:
  - LangChain
  - Streamlit
- **Vector Store**: Chroma
- **Embeddings**: Hugging Face (`all-MiniLM-L6-v2`)
- **LLMs**:
  - Groq (default)
  - OpenRouter (OpenAI-compatible)
  - Hugging Face Inference API
- **Environment Management**: `python-dotenv`

---

## 🚀 Getting Started

### 1️⃣ Clone the repository

- git clone https://github.com/your-username/policy-RAG-BOT.git
- cd policy-RAG-BOT

## 🚀 Getting Started

### 2️⃣ Create and activate a virtual environment

- python -m venv .venv
- source .venv/bin/activate  # macOS/Linux

### 3️⃣ Install dependencies
- pip install -r requirements.txt

### 4️⃣ Configure environment variables
- This project does not ship with API keys.
- Copy the example environment file:

- cp example.env .env
- Edit .env to choose your LLM provider:

### Preparing the Vector Database

The current demo uses one official press release:
Year-End Review 2024: Ministry of Environment, Forest and Climate Change (India)
(https://www.pib.gov.in/PressReleasePage.aspx?PRID=2088406&utm_source=chatgpt.com&reg=3&lang=2)

### To generate the vector database, run:

- python vectordb.py

- This step:
- Loads the policy document
- Generates embeddings
- Persists them to the vector_db/ directory
- You may replace or extend this with any government policy PDF or document.

### 💬 Running the Application

- With memory-enabled chatbot
- streamlit run bot.py
- Stateless version (no memory)
- Streamlit run test.py

### Demo 
- Example Question:
- How many projects were sanctioned overall during 2024 by Ministry of environment?
- Expected Behavior:
- Answers strictly from retrieved policy context
- Refuses politely if information is missing
- Suggests related policy information when refusing

### 📁 Project Structure
- policy-RAG-BOT/
- ├── bot.py                # Streamlit app with chat memory
- ├── test.py               # Stateless version
- ├── vectordb.py           # Document ingestion & vector DB creation
- ├── vector_db/            # Persisted Chroma embeddings
- ├── example.env           # Environment variable template
- ├── requirements.txt
- └── README.md

### 🛣️ Roadmap (v2 – Work in Progress)
- Planned enhancements:
- Evaluation of chatbot
- Query rewriting & semantic expansion
- Conflict detection across documents
- Failure-aware reasoning paths
- Multi-document comparison
- Hybrid retrieval strategies
- Explicit source attribution
