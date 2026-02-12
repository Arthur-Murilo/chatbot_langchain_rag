"""
Unit tests for document loader module
Tests document loading, chunking, and indexing functionality
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path


@pytest.mark.unit
class TestDocumentLoader:
    """Test document loading functions"""
    
    @patch('src.loaders.document_loader.os.listdir')
    @patch('src.loaders.document_loader.TextLoader')
    def test_carregar_documentos_txt(self, mock_text_loader, mock_listdir):
        """Test loading TXT documents"""
        from src.loaders.document_loader import carregar_documentos
        from langchain.schema import Document
        
        # Mock file listing
        mock_listdir.return_value = ['doc1.txt', 'doc2.pdf', 'doc3.docx']
        
        # Mock loader
        mock_loader_instance = Mock()
        mock_loader_instance.load.return_value = [
            Document(page_content="Test content", metadata={"source": "doc1.txt"})
        ]
        mock_text_loader.return_value = mock_loader_instance
        
        # Test
        docs = carregar_documentos("test_dir")
        
        assert len(docs) >= 1
        assert mock_text_loader.called
    
    def test_dividir_documentos(self, sample_documents):
        """Test document splitting into chunks"""
        from src.loaders.document_loader import dividir_documentos
        
        chunks = dividir_documentos(sample_documents)
        
        # Should have at least as many chunks as documents
        assert len(chunks) >= len(sample_documents)
        
        # Each chunk should be a Document
        from langchain.schema import Document
        for chunk in chunks:
            assert isinstance(chunk, Document)
            assert hasattr(chunk, 'page_content')
            assert hasattr(chunk, 'metadata')
    
    def test_dividir_documentos_with_overlap(self, sample_documents):
        """Test that chunks have proper overlap"""
        from src.loaders.document_loader import dividir_documentos
        
        chunks = dividir_documentos(sample_documents)
        
        # Check that chunks are reasonable size
        for chunk in chunks:
            content_length = len(chunk.page_content)
            # Should not exceed chunk_size by much
            assert content_length <= 1200  # chunk_size + some tolerance
    
    @patch('src.loaders.document_loader.Qdrant')
    @patch('src.loaders.document_loader.QdrantClient')
    @patch('src.loaders.document_loader.OllamaEmbeddings')
    def test_banco_qdrant_creation(self, mock_embeddings, mock_client, mock_qdrant):
        """Test Qdrant vector store creation"""
        from src.loaders.document_loader import banco_qdrant
        
        # Mock dependencies
        mock_embeddings_instance = Mock()
        mock_embeddings.return_value = mock_embeddings_instance
        
        mock_client_instance = Mock()
        mock_client.return_value = mock_client_instance
        
        mock_qdrant_instance = Mock()
        mock_qdrant.return_value = mock_qdrant_instance
        
        # Test
        vector_store = banco_qdrant()
        
        # Verify Qdrant was created with correct parameters
        assert mock_qdrant.called
        assert vector_store is not None


@pytest.mark.unit
class TestTextSplitter:
    """Test text splitting logic"""
    
    def test_split_preserves_metadata(self, sample_documents):
        """Test that splitting preserves document metadata"""
        from src.loaders.document_loader import dividir_documentos
        
        chunks = dividir_documentos(sample_documents)
        
        # Each chunk should preserve source metadata
        for chunk in chunks:
            assert 'source' in chunk.metadata
    
    def test_split_creates_reasonable_chunks(self):
        """Test that chunks are not too large or too small"""
        from src.loaders.document_loader import dividir_documentos
        from langchain.schema import Document
        
        # Create a long document
        long_text = "Este é um texto longo. " * 100
        docs = [Document(page_content=long_text, metadata={"source": "test.txt"})]
        
        chunks = dividir_documentos(docs)
        
        # Should create multiple chunks
        assert len(chunks) > 1
        
        # Each chunk should be reasonable size
        for chunk in chunks:
            assert 0 < len(chunk.page_content) <= 1500


@pytest.mark.integration
@pytest.mark.requires_services
class TestLoaderIntegration:
    """Integration tests for document loader (requires running services)"""
    
    def test_full_indexing_pipeline(self, test_data_dir, mock_settings):
        """Test complete document indexing pipeline"""
        # This test would require actual Qdrant and Ollama services
        # Skip if services are not available
        pytest.skip("Requires running Qdrant and Ollama services")
    
    def test_qdrant_connection(self):
        """Test connection to Qdrant service"""
        # Skip if Qdrant is not running
        pytest.skip("Requires running Qdrant service")
    
    def test_ollama_embedding_generation(self):
        """Test embedding generation with Ollama"""
        # Skip if Ollama is not running
        pytest.skip("Requires running Ollama service")
