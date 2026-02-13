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

## 🤖 Chatbot Capabilities

Policy-RAG-BOT is designed to:

### Supported
- Answer questions strictly from ingested policy documents  
- Maintain conversation memory (memory-enabled version)  
- Support multiple LLM providers  
- Refuse questions not supported by retrieved context  

### Not Supported
- Answering questions outside ingested documents  
- Accessing live government databases  
- Performing autonomous browsing or policy updates  

This ensures transparency and grounded responses.

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
- **Streamlit-based UI** for conversational interaction  
- **Centralized configuration via `config.py`**  
- **Query preprocessing for improved retrieval accuracy**  
- **Retrieval evaluation framework**

---

## 🏗️ Architecture Overview

1. Policy documents are embedded using **Hugging Face sentence transformers**
2. Embeddings are stored in a **Chroma vector database**
3. User queries are:
   - Preprocessed for consistency
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

## 📁 Project Structure
```
RAG-BOT-MEMORY/
│
├── main.py              # Streamlit chatbot application
├── vectordb.py          # Document ingestion and vector database creation
├── config.py            # Centralized configuration for embeddings, chunking, retrieval
├── query_utils.py       # Query preprocessing module
├── evaluate.py          # Retrieval evaluation script
│
├── requirements.txt     # Project dependencies
├── example.env          # Environment variable template
│
├── data/                # Policy documents for ingestion
├── vector_db/           # Persisted Chroma vector database
```

---

## ⚙️ Configuration

The system uses a centralized configuration file (`config.py`) to manage key parameters.

Example configuration:
```python
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
RETRIEVAL_K = 4
VECTOR_DB_DIR = "vector_db"
```

This allows easy tuning of retrieval, chunking, and embedding behavior without modifying core logic.

---

## 🚀 Getting Started

### 1️⃣ Clone the repository
```bash
git clone https://github.com/nisg-phys/RAG-BOT-MEMORY.git
cd RAG-BOT-MEMORY
```

### 2️⃣ Create and activate virtual environment
```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Configure environment variables

Copy the example environment file:
```bash
cp example.env .env
```

Edit `.env` and choose your LLM provider.

---

## 📄 Preparing the Vector Database

The current demo uses the official press release:

**Year-End Review 2024: Ministry of Environment, Forest and Climate Change (India)**  
https://www.pib.gov.in/PressReleasePage.aspx?PRID=2088406

To generate the vector database:
```bash
python vectordb.py
```

This step:
- Loads policy documents from `data/`
- Splits them into chunks
- Generates embeddings
- Stores them in `vector_db/`

You may extend this with any government policy document.

---

## 🔎 Query Processing

User queries are preprocessed using `query_utils.py` before retrieval.

Current preprocessing includes:
- Removing extra whitespace
- Normalizing query formatting

This improves retrieval consistency and enables future enhancements such as:
- Query rewriting
- Semantic expansion
- Query normalization

---

## 📊 Retrieval Evaluation

Retrieval performance can be evaluated using:
```bash
python evaluate.py
```

This script:
- Tests retrieval on sample queries
- Displays retrieved document chunks
- Verifies grounding quality

Example output:
```
Query: What environmental schemes were introduced in 2024?
Retrieved chunks: 4
Top chunk preview: The Ministry launched...
```

This ensures the system retrieves relevant and grounded information.

---

## 💬 Running the Application

Start the chatbot:
```bash
streamlit run main.py
```

---

## 🧪 Example Usage

**Example Question:**
> How many projects were sanctioned overall during 2024?

**Expected Behavior:**
- Answers strictly from retrieved policy context
- Refuses politely if information is missing
- Suggests related policy information when refusing

---

## 🔧 Extensibility

The system is modular and supports:
- Adding new policy documents without code changes
- Switching embedding models via `config.py`
- Switching LLM providers
- Evaluating retrieval quality
- Extending query preprocessing

---

## 🛣️ Roadmap (v2 – Work in Progress)

Planned enhancements:
- Advanced retrieval evaluation metrics
- Query rewriting & semantic expansion
- Hybrid keyword + semantic search
- Multi-document comparison
- Explicit source attribution
- Conflict detection across policy documents

---

## 📜 License

This project is open-source and available for research and educational use.