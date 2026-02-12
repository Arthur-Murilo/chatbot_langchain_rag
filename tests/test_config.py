"""
Unit tests for configuration module
Tests settings loading, validation, and environment variables
"""

import pytest
import os
from unittest.mock import patch, Mock


@pytest.mark.unit
class TestSettings:
    """Test Settings class"""
    
    def test_settings_loads_from_env(self):
        """Test that settings load from environment variables"""
        with patch.dict(os.environ, {
            'GROQ_API_KEY': 'test_key',
            'LLM_MODEL': 'test_model',
            'QDRANT_URL': 'http://test:6333'
        }):
            from src.config.settings import settings
            
            assert settings.GROQ_API_KEY == 'test_key'
            assert settings.LLM_MODEL == 'test_model'
            assert settings.QDRANT_URL == 'http://test:6333'
    
    def test_settings_has_required_attributes(self):
        """Test that settings has all required attributes"""
        from src.config.settings import settings
        
        required_attrs = [
            'GROQ_API_KEY',
            'LLM_MODEL',
            'LLM_TEMPERATURE',
            'LLM_MAX_TOKENS',
            'OLLAMA_MODEL',
            'OLLAMA_BASE_URL',
            'QDRANT_URL',
            'QDRANT_COLLECTION',
            'MONGO_USER',
            'MONGO_PASSWORD',
            'MONGO_HOST',
            'MONGO_PORT',
            'MONGO_DATABASE',
            'MONGO_COLLECTION'
        ]
        
        for attr in required_attrs:
            assert hasattr(settings, attr), f"Settings missing attribute: {attr}"
    
    def test_mongo_uri_generation(self):
        """Test MongoDB URI generation"""
        from src.config.settings import settings
        
        uri = settings.get_mongo_uri()
        
        assert uri is not None
        assert 'mongodb://' in uri
        assert settings.MONGO_HOST in uri
        assert str(settings.MONGO_PORT) in uri
    
    def test_temperature_is_float(self):
        """Test that temperature is a float between 0 and 1"""
        from src.config.settings import settings
        
        assert isinstance(settings.LLM_TEMPERATURE, float)
        assert 0.0 <= settings.LLM_TEMPERATURE <= 1.0
    
    def test_max_tokens_is_int(self):
        """Test that max_tokens is a positive integer"""
        from src.config.settings import settings
        
        assert isinstance(settings.LLM_MAX_TOKENS, int)
        assert settings.LLM_MAX_TOKENS > 0


@pytest.mark.unit
class TestPrompts:
    """Test prompt configurations"""
    
    def test_system_prompt_exists(self):
        """Test that system prompt is defined"""
        from src.config.prompts import SYSTEM_PROMPT
        
        assert SYSTEM_PROMPT is not None
        assert len(SYSTEM_PROMPT) > 0
        assert isinstance(SYSTEM_PROMPT, str)
    
    def test_system_prompt_contains_role(self):
        """Test that system prompt defines the assistant role"""
        from src.config.prompts import SYSTEM_PROMPT
        
        # Should mention being a personal trainer or fitness assistant
        keywords = ['personal trainer', 'fitness', 'treino', 'musculação']
        assert any(keyword.lower() in SYSTEM_PROMPT.lower() for keyword in keywords)
