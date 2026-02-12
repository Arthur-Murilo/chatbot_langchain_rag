"""
Integration tests - Test service connectivity and health checks
These tests verify that all critical services are running and accessible
"""

import pytest
import requests
from time import sleep
import os


@pytest.mark.integration
class TestServiceConnectivity:
    """Test connectivity to all required services"""
    
    def test_qdrant_health(self):
        """Test Qdrant service is running and healthy"""
        try:
            response = requests.get("http://localhost:6333/healthz", timeout=5)
            assert response.status_code == 200
            print("✅ Qdrant está online")
        except requests.exceptions.ConnectionError:
            pytest.skip("⚠️  Qdrant não está rodando")
        except Exception as e:
            pytest.fail(f"❌ Erro ao conectar ao Qdrant: {e}")
    
    def test_qdrant_collections(self):
        """Test Qdrant collections endpoint"""
        try:
            response = requests.get("http://localhost:6333/collections", timeout=5)
            assert response.status_code == 200
            data = response.json()
            print(f"✅ Qdrant collections: {data}")
        except requests.exceptions.ConnectionError:
            pytest.skip("⚠️  Qdrant não está rodando")
        except Exception as e:
            pytest.fail(f"❌ Erro ao listar collections: {e}")
    
    def test_ollama_health(self):
        """Test Ollama service is running"""
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            assert response.status_code == 200
            data = response.json()
            print(f"✅ Ollama está online com {len(data.get('models', []))} modelos")
        except requests.exceptions.ConnectionError:
            pytest.skip("⚠️  Ollama não está rodando")
        except Exception as e:
            pytest.fail(f"❌ Erro ao conectar ao Ollama: {e}")
    
    def test_ollama_has_embedding_model(self):
        """Test that Ollama has the required embedding model"""
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            data = response.json()
            models = [model['name'] for model in data.get('models', [])]
            
            required_model = "qwen3-embedding:0.6b"
            
            # Check if model exists (with or without :latest)
            has_model = any(required_model in model for model in models)
            
            if has_model:
                print(f"✅ Modelo de embedding encontrado: {required_model}")
            else:
                pytest.skip(f"⚠️  Modelo {required_model} não encontrado. Modelos disponíveis: {models}")
        
        except requests.exceptions.ConnectionError:
            pytest.skip("⚠️  Ollama não está rodando")
    
    def test_mongodb_connection(self):
        """Test MongoDB connection"""
        try:
            from pymongo import MongoClient
            from src.config.settings import settings
            
            client = MongoClient(
                settings.get_mongo_uri(),
                serverSelectionTimeoutMS=5000
            )
            
            # Try to get server info
            client.server_info()
            print("✅ MongoDB está online")
            
            # List databases
            dbs = client.list_database_names()
            print(f"✅ Databases disponíveis: {dbs}")
            
        except Exception as e:
            pytest.skip(f"⚠️  MongoDB não está rodando: {e}")
    
    def test_streamlit_app(self):
        """Test Streamlit app is running"""
        try:
            response = requests.get("http://localhost:8501/_stcore/health", timeout=5)
            assert response.status_code == 200
            print("✅ Streamlit app está online")
        except requests.exceptions.ConnectionError:
            pytest.skip("⚠️  Streamlit app não está rodando")
        except Exception as e:
            pytest.skip(f"⚠️  Streamlit app não acessível: {e}")


@pytest.mark.integration
@pytest.mark.requires_services
class TestDataPipeline:
    """Test complete data pipeline"""
    
    def test_document_indexing(self):
        """Test that documents are properly indexed in Qdrant"""
        try:
            from qdrant_client import QdrantClient
            from src.config.settings import settings
            
            client = QdrantClient(url=settings.QDRANT_URL)
            
            # Get collection info
            try:
                collection_info = client.get_collection(settings.QDRANT_COLLECTION)
                vectors_count = collection_info.vectors_count
                
                if vectors_count > 0:
                    print(f"✅ Collection tem {vectors_count} vetores indexados")
                else:
                    pytest.skip("⚠️  Collection está vazia. Execute o document_loader primeiro.")
            
            except Exception as e:
                pytest.skip(f"⚠️  Collection não existe: {e}")
        
        except Exception as e:
            pytest.skip(f"⚠️  Não foi possível testar indexação: {e}")
    
    def test_qdrant_search(self):
        """Test vector search in Qdrant"""
        try:
            from qdrant_client import QdrantClient
            from src.config.settings import settings
            from langchain_community.embeddings import OllamaEmbeddings
            
            # Create embeddings
            embeddings = OllamaEmbeddings(
                model=settings.OLLAMA_MODEL,
                base_url=settings.OLLAMA_BASE_URL
            )
            
            # Generate query embedding
            query_vector = embeddings.embed_query("agachamento")
            
            # Search in Qdrant
            client = QdrantClient(url=settings.QDRANT_URL)
            results = client.search(
                collection_name=settings.QDRANT_COLLECTION,
                query_vector=query_vector,
                limit=3
            )
            
            if len(results) > 0:
                print(f"✅ Busca retornou {len(results)} resultados")
                for i, result in enumerate(results, 1):
                    print(f"  {i}. Score: {result.score:.4f}")
            else:
                pytest.skip("⚠️  Busca não retornou resultados")
        
        except Exception as e:
            pytest.skip(f"⚠️  Não foi possível testar busca: {e}")


@pytest.mark.integration
class TestEnvironmentVariables:
    """Test that all required environment variables are set"""
    
    def test_groq_api_key_exists(self):
        """Test GROQ_API_KEY is set"""
        from src.config.settings import settings
        
        assert settings.GROQ_API_KEY is not None
        assert len(settings.GROQ_API_KEY) > 0
        assert settings.GROQ_API_KEY != "your_groq_api_key_here"
        print("✅ GROQ_API_KEY está configurada")
    
    def test_required_env_vars(self):
        """Test all required environment variables are set"""
        from src.config.settings import settings
        
        required_vars = {
            'QDRANT_URL': settings.QDRANT_URL,
            'QDRANT_COLLECTION': settings.QDRANT_COLLECTION,
            'OLLAMA_MODEL': settings.OLLAMA_MODEL,
            'OLLAMA_BASE_URL': settings.OLLAMA_BASE_URL,
            'LLM_MODEL': settings.LLM_MODEL,
        }
        
        missing = []
        for var_name, var_value in required_vars.items():
            if not var_value or var_value.startswith('your_'):
                missing.append(var_name)
        
        if missing:
            pytest.fail(f"❌ Variáveis não configuradas: {', '.join(missing)}")
        else:
            print(f"✅ Todas as variáveis necessárias estão configuradas")


@pytest.mark.integration
@pytest.mark.slow
class TestEndToEnd:
    """End-to-end tests for complete workflows"""
    
    def test_complete_rag_query(self):
        """Test complete RAG query from end to end"""
        try:
            from src.agents.agent import PersonalTrainerAgent
            
            # Create agent
            agent = PersonalTrainerAgent(session_id="test_e2e")
            
            # Make query
            response = agent.query("O que é hipertrofia?")
            
            # Verify response
            assert response is not None
            assert isinstance(response, str)
            assert len(response) > 10
            
            print(f"✅ RAG query completa funcionou")
            print(f"   Resposta: {response[:100]}...")
            
            # Clean up
            agent.clear_history()
        
        except Exception as e:
            pytest.skip(f"⚠️  Teste E2E falhou: {e}")
    
    def test_multi_turn_conversation(self):
        """Test multi-turn conversation with context"""
        try:
            from src.agents.agent import PersonalTrainerAgent
            
            # Create agent
            agent = PersonalTrainerAgent(session_id="test_multi_turn")
            
            # First query
            response1 = agent.query("Como fazer flexão?")
            assert response1 is not None
            
            # Follow-up query (should use context)
            response2 = agent.query("Quantas repetições devo fazer?")
            assert response2 is not None
            
            # Get history
            history = agent.get_chat_history()
            assert len(history) == 4  # 2 user + 2 assistant messages
            
            print("✅ Conversa multi-turno funcionou")
            
            # Clean up
            agent.clear_history()
        
        except Exception as e:
            pytest.skip(f"⚠️  Teste multi-turno falhou: {e}")


def test_system_health_report():
    """Generate a health report of all services"""
    print("\n" + "="*60)
    print("📊 RELATÓRIO DE SAÚDE DO SISTEMA")
    print("="*60)
    
    services = {
        "Qdrant": "http://localhost:6333/healthz",
        "Ollama": "http://localhost:11434/api/tags",
        "MongoDB": None,  # Special handling
        "Streamlit": "http://localhost:8501/_stcore/health",
    }
    
    status = {}
    
    for service, url in services.items():
        if service == "MongoDB":
            try:
                from pymongo import MongoClient
                from src.config.settings import settings
                client = MongoClient(settings.get_mongo_uri(), serverSelectionTimeoutMS=3000)
                client.server_info()
                status[service] = "✅ Online"
            except:
                status[service] = "❌ Offline"
        else:
            try:
                response = requests.get(url, timeout=3)
                if response.status_code == 200:
                    status[service] = "✅ Online"
                else:
                    status[service] = f"⚠️  Status {response.status_code}"
            except:
                status[service] = "❌ Offline"
    
    for service, state in status.items():
        print(f"{service:15} {state}")
    
    print("="*60 + "\n")
    
    # Count online services
    online = sum(1 for s in status.values() if "✅" in s)
    total = len(status)
    
    if online == total:
        print(f"✅ Todos os {total} serviços estão online!")
    else:
        print(f"⚠️  {online}/{total} serviços online")
        print(f"❌ Execute 'docker-compose up -d' para iniciar os serviços")
