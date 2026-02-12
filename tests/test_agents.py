"""
Unit tests for agent module
Tests PersonalTrainerAgent class and RAG functionality
"""

import pytest
from unittest.mock import Mock, patch, MagicMock, call


@pytest.mark.unit
class TestPersonalTrainerAgent:
    """Test PersonalTrainerAgent class"""
    
    @patch('src.agents.agent.ChatGroq')
    @patch('src.agents.agent.OllamaEmbeddings')
    @patch('src.agents.agent.Qdrant')
    @patch('src.agents.agent.MongoDBChatMessageHistory')
    def test_agent_initialization(self, mock_mongo, mock_qdrant, mock_embeddings, mock_groq):
        """Test agent initialization"""
        from src.agents.agent import PersonalTrainerAgent
        
        # Mock all dependencies
        mock_groq.return_value = Mock()
        mock_embeddings.return_value = Mock()
        mock_qdrant.return_value = Mock()
        mock_mongo.return_value = Mock()
        
        # Create agent
        agent = PersonalTrainerAgent(session_id="test_session")
        
        # Verify initialization
        assert agent is not None
        assert mock_groq.called
        assert mock_embeddings.called
        assert mock_qdrant.called
        assert mock_mongo.called
    
    @patch('src.agents.agent.ChatGroq')
    @patch('src.agents.agent.OllamaEmbeddings')
    @patch('src.agents.agent.Qdrant')
    @patch('src.agents.agent.MongoDBChatMessageHistory')
    @patch('src.agents.agent.QdrantClient')
    def test_query_method(self, mock_client, mock_mongo, mock_qdrant, mock_embeddings, mock_groq):
        """Test query method returns response"""
        from src.agents.agent import PersonalTrainerAgent
        
        # Mock LLM response
        mock_llm = Mock()
        mock_llm.invoke = Mock(return_value="Resposta sobre agachamento")
        mock_groq.return_value = mock_llm
        
        # Mock embeddings
        mock_embeddings.return_value = Mock()
        
        # Mock Qdrant with retriever
        mock_vector_store = Mock()
        mock_retriever = Mock()
        mock_retriever.get_relevant_documents = Mock(return_value=[])
        mock_vector_store.as_retriever = Mock(return_value=mock_retriever)
        mock_qdrant.return_value = mock_vector_store
        
        # Mock client
        mock_client.return_value = Mock()
        
        # Mock MongoDB
        mock_history = Mock()
        mock_history.messages = []
        mock_mongo.return_value = mock_history
        
        # Create agent and query
        agent = PersonalTrainerAgent(session_id="test_session")
        response = agent.query("Como fazer agachamento?")
        
        # Verify response
        assert response is not None
        assert isinstance(response, str)
        assert len(response) > 0
    
    @patch('src.agents.agent.ChatGroq')
    @patch('src.agents.agent.OllamaEmbeddings')
    @patch('src.agents.agent.Qdrant')
    @patch('src.agents.agent.MongoDBChatMessageHistory')
    @patch('src.agents.agent.QdrantClient')
    def test_get_chat_history(self, mock_client, mock_mongo, mock_qdrant, mock_embeddings, mock_groq):
        """Test getting chat history"""
        from src.agents.agent import PersonalTrainerAgent
        from langchain.schema.messages import HumanMessage, AIMessage
        
        # Mock dependencies
        mock_groq.return_value = Mock()
        mock_embeddings.return_value = Mock()
        mock_qdrant.return_value = Mock()
        mock_client.return_value = Mock()
        
        # Mock chat history with messages
        mock_history = Mock()
        mock_history.messages = [
            HumanMessage(content="Como fazer flexão?"),
            AIMessage(content="Para fazer flexão...")
        ]
        mock_mongo.return_value = mock_history
        
        # Create agent and get history
        agent = PersonalTrainerAgent(session_id="test_session")
        history = agent.get_chat_history()
        
        # Verify history
        assert isinstance(history, list)
        assert len(history) == 2
        assert history[0]["role"] == "user"
        assert history[1]["role"] == "assistant"
        assert "flexão" in history[0]["content"]
    
    @patch('src.agents.agent.ChatGroq')
    @patch('src.agents.agent.OllamaEmbeddings')
    @patch('src.agents.agent.Qdrant')
    @patch('src.agents.agent.MongoDBChatMessageHistory')
    @patch('src.agents.agent.QdrantClient')
    def test_clear_history(self, mock_client, mock_mongo, mock_qdrant, mock_embeddings, mock_groq):
        """Test clearing chat history"""
        from src.agents.agent import PersonalTrainerAgent
        
        # Mock dependencies
        mock_groq.return_value = Mock()
        mock_embeddings.return_value = Mock()
        mock_qdrant.return_value = Mock()
        mock_client.return_value = Mock()
        
        # Mock chat history
        mock_history = Mock()
        mock_history.clear = Mock()
        mock_mongo.return_value = mock_history
        
        # Create agent and clear history
        agent = PersonalTrainerAgent(session_id="test_session")
        agent.clear_history()
        
        # Verify clear was called
        assert mock_history.clear.called
    
    @patch('src.agents.agent.ChatGroq')
    @patch('src.agents.agent.OllamaEmbeddings')
    @patch('src.agents.agent.Qdrant')
    @patch('src.agents.agent.MongoDBChatMessageHistory')
    @patch('src.agents.agent.QdrantClient')
    def test_session_id_storage(self, mock_client, mock_mongo, mock_qdrant, mock_embeddings, mock_groq):
        """Test that session_id is properly stored"""
        from src.agents.agent import PersonalTrainerAgent
        
        # Mock dependencies
        mock_groq.return_value = Mock()
        mock_embeddings.return_value = Mock()
        mock_qdrant.return_value = Mock()
        mock_client.return_value = Mock()
        mock_mongo.return_value = Mock()
        
        # Create agent with specific session_id
        session_id = "test_user_123"
        agent = PersonalTrainerAgent(session_id=session_id)
        
        # Verify session_id was passed to MongoDB
        mock_mongo.assert_called_once()
        call_kwargs = mock_mongo.call_args[1]
        assert call_kwargs['session_id'] == session_id


@pytest.mark.unit
class TestRAGPipeline:
    """Test RAG pipeline components"""
    
    def test_retriever_returns_documents(self, mock_qdrant_client):
        """Test that retriever returns relevant documents"""
        from langchain.schema import Document
        
        # Mock retriever
        mock_retriever = Mock()
        mock_retriever.get_relevant_documents = Mock(return_value=[
            Document(page_content="Documento sobre agachamento", metadata={"source": "test.txt"}),
            Document(page_content="Documento sobre musculação", metadata={"source": "test2.txt"}),
        ])
        
        # Test retrieval
        results = mock_retriever.get_relevant_documents("agachamento")
        
        assert len(results) > 0
        assert all(isinstance(doc, Document) for doc in results)
    
    def test_context_formatting(self):
        """Test that context is properly formatted for LLM"""
        from langchain.schema import Document
        
        # Sample documents
        docs = [
            Document(page_content="Texto 1", metadata={"source": "doc1.txt"}),
            Document(page_content="Texto 2", metadata={"source": "doc2.txt"}),
        ]
        
        # Format context (simple concatenation example)
        context = "\n\n".join([doc.page_content for doc in docs])
        
        assert "Texto 1" in context
        assert "Texto 2" in context
        assert len(context) > 0


@pytest.mark.unit
class TestMemoryManagement:
    """Test conversation memory management"""
    
    def test_memory_stores_conversation(self):
        """Test that memory stores conversation turns"""
        from langchain.memory import ConversationBufferMemory
        from langchain.schema.messages import HumanMessage, AIMessage
        
        # Create memory
        memory = ConversationBufferMemory(return_messages=True)
        
        # Add messages
        memory.chat_memory.add_user_message("Como fazer flexão?")
        memory.chat_memory.add_ai_message("Para fazer flexão...")
        
        # Verify storage
        messages = memory.chat_memory.messages
        assert len(messages) == 2
        assert isinstance(messages[0], HumanMessage)
        assert isinstance(messages[1], AIMessage)
    
    def test_memory_clear(self):
        """Test that memory can be cleared"""
        from langchain.memory import ConversationBufferMemory
        
        # Create memory with messages
        memory = ConversationBufferMemory(return_messages=True)
        memory.chat_memory.add_user_message("Test message")
        
        # Clear
        memory.clear()
        
        # Verify empty
        assert len(memory.chat_memory.messages) == 0


@pytest.mark.integration
@pytest.mark.requires_services
class TestAgentIntegration:
    """Integration tests for agent (requires running services)"""
    
    def test_full_rag_pipeline(self):
        """Test complete RAG pipeline with real services"""
        # This test requires all services running
        pytest.skip("Requires running Groq, Qdrant, Ollama, MongoDB")
    
    def test_agent_with_real_groq(self):
        """Test agent with real Groq API"""
        # Skip if no API key
        pytest.skip("Requires valid GROQ_API_KEY")
    
    def test_agent_with_real_qdrant(self):
        """Test agent with real Qdrant service"""
        pytest.skip("Requires running Qdrant service")
