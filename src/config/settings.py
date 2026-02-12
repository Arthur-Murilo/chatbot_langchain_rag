import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    MONGO_USER = os.getenv("MONGO_USER", "admin")
    MONGO_PASSWORD = os.getenv("MONGO_PASSWORD", "admin")
    MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
    MONGO_PORT = os.getenv("MONGO_PORT", "27017")
    MONGO_DATABASE = os.getenv("MONGO_DATABASE", "chat_history")
    MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "message_store")
    
    @property
    def MONGO_CONNECTION_STRING(self):
        return f"mongodb://{self.MONGO_USER}:{self.MONGO_PASSWORD}@{self.MONGO_HOST}:{self.MONGO_PORT}"
    
    QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
    QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "rag_gym_personal")
    
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3-embedding:0.6b")
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    
    LLM_MODEL = os.getenv("LLM_MODEL", "openai/gpt-oss-120b")
    LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.7"))
    LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "1000"))


settings = Settings()
