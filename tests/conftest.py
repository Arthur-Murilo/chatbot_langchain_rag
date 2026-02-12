# Test configuration and shared fixtures
import pytest
import os
from unittest.mock import Mock, MagicMock
from dotenv import load_dotenv

# Load test environment variables
load_dotenv()


@pytest.fixture
def mock_settings():
    """Mock settings for testing"""
    settings = Mock()
    settings.GROQ_API_KEY = "test_key_123"
    settings.LLM_MODEL = "openai/gpt-oss-120b"
    settings.LLM_TEMPERATURE = 0.7
    settings.LLM_MAX_TOKENS = 1000
    settings.OLLAMA_MODEL = "qwen3-embedding:0.6b"
    settings.OLLAMA_BASE_URL = "http://localhost:11434"
    settings.QDRANT_URL = "http://localhost:6333"
    settings.QDRANT_COLLECTION = "test_collection"
    settings.MONGO_USER = "test_user"
    settings.MONGO_PASSWORD = "test_pass"
    settings.MONGO_HOST = "localhost"
    settings.MONGO_PORT = 27017
    settings.MONGO_DATABASE = "test_db"
    settings.MONGO_COLLECTION = "test_collection"
    settings.get_mongo_uri = Mock(return_value="mongodb://test:test@localhost:27017")
    return settings


@pytest.fixture
def mock_ollama_embeddings():
    """Mock Ollama embeddings"""
    embeddings = MagicMock()
    embeddings.embed_query = Mock(return_value=[0.1] * 768)
    embeddings.embed_documents = Mock(return_value=[[0.1] * 768, [0.2] * 768])
    return embeddings


@pytest.fixture
def mock_qdrant_client():
    """Mock Qdrant client"""
    client = MagicMock()
    client.get_collection = Mock(return_value={"vectors_count": 100})
    client.search = Mock(return_value=[])
    return client


@pytest.fixture
def mock_groq_llm():
    """Mock Groq LLM"""
    llm = MagicMock()
    llm.invoke = Mock(return_value="Mocked response from LLM")
    return llm


@pytest.fixture
def sample_documents():
    """Sample documents for testing"""
    from langchain.schema import Document
    
    return [
        Document(
            page_content="O agachamento é um exercício fundamental para membros inferiores.",
            metadata={"source": "data/test_doc1.txt"}
        ),
        Document(
            page_content="A flexão é excelente para fortalecer peitoral e tríceps.",
            metadata={"source": "data/test_doc2.txt"}
        ),
        Document(
            page_content="O supino é um dos melhores exercícios para desenvolvimento peitoral.",
            metadata={"source": "data/test_doc3.txt"}
        ),
    ]


@pytest.fixture
def sample_chunks():
    """Sample document chunks for testing"""
    from langchain.schema import Document
    
    return [
        Document(
            page_content="Chunk 1 sobre agachamento",
            metadata={"source": "data/test.txt", "chunk_id": 0}
        ),
        Document(
            page_content="Chunk 2 sobre flexão",
            metadata={"source": "data/test.txt", "chunk_id": 1}
        ),
    ]


@pytest.fixture(scope="session")
def test_data_dir(tmp_path_factory):
    """Create temporary directory for test data"""
    data_dir = tmp_path_factory.mktemp("test_data")
    
    # Create sample files
    (data_dir / "test_doc.txt").write_text(
        "Este é um documento de teste sobre musculação e fitness."
    )
    
    return data_dir


def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
    config.addinivalue_line(
        "markers", "requires_services: mark test as requiring external services"
    )
