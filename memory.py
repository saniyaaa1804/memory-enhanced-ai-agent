
from pathlib import Path
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma


class MemoryManager:

    def __init__(self):
        self.short_term_memory = []

        self.embedding_model = OllamaEmbeddings(
            model="nomic-embed-text"
        )

        self.db_path = Path(__file__).parent / "database" / "chroma_db"
        self.db_path.mkdir(parents=True, exist_ok=True)

        self.vector_db = Chroma(
            collection_name="agent_long_term_memory",
            embedding_function=self.embedding_model,
            persist_directory=str(self.db_path)
        )

    def add_to_short_term(self, role, message):
        self.short_term_memory.append({
            "role": role,
            "message": message
        })

        self.short_term_memory = self.short_term_memory[-10:]

    def get_short_term_memory(self):
        return self.short_term_memory

    def add_to_long_term(self, information):
        self.vector_db.add_texts(
            texts=[information],
            metadatas=[{"source": "conversation"}]
        )

    def search_long_term(self, query, k=3):
        results = self.vector_db.similarity_search(query, k=k)
        return [doc.page_content for doc in results]

    def clear_short_term(self):
        self.short_term_memory = []

    def get_all_recent_memories(self, limit=10):
        data = self.vector_db.get(
            limit=limit,
            include=["documents"]
        )
        return data.get("documents", [])
