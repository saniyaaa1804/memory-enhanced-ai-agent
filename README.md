
# Memory-Enhanced AI Agent

## Project Overview

Memory-Enhanced AI Agent is a Python-based AI application developed using Streamlit, LangChain, Ollama and ChromaDB.

The application demonstrates short-term memory, persistent long-term memory, semantic retrieval and external tool integration.

## Features

- Short-term conversation memory
- Long-term memory using ChromaDB
- Semantic search using Ollama embeddings
- Local LLM using Qwen 2.5 3B
- Web search integration
- Calculator tool
- Memory-enabled vs memoryless comparison
- Agent activity log

## Technology Stack

- Python
- Streamlit
- LangChain
- Ollama
- Qwen 2.5 3B
- ChromaDB
- Nomic Embed Text
- DuckDuckGo Search

## Installation

Clone the repository:

```bash
git clone YOUR_REPOSITORY_URL
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Download Ollama models:

```bash
ollama pull qwen2.5:3b
ollama pull nomic-embed-text
```

Run the application:

```bash
streamlit run app.py
```

## Tool Commands

Calculator:

```text
calculate: 250 * 4 + 100
```

Web Search:

```text
search: Latest developments in artificial intelligence
```

## Memory Architecture

Short-term memory maintains recent conversation messages.

Long-term memory stores conversation information in ChromaDB and retrieves relevant information using semantic similarity.

## Learning Outcomes

- Understanding short-term and long-term memory.
- Implementing vector-store-based retrieval.
- Integrating external tools into an AI application.
- Comparing memory-enabled and memoryless responses.
- Understanding environment interaction.

## Author

Om Akolkar

B.Tech Computer Science and Engineering
AI and Analytics
MIT ADT University, Pune
