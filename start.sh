#!/bin/bash

echo "🚀 Iniciando Personal Trainer AI - Sistema RAG"
echo ""

if [ ! -f .env ]; then
    echo "⚠️  Arquivo .env não encontrado. Criando a partir do .env.example..."
    cp .env.example .env
    echo "✅ Arquivo .env criado. Por favor, configure suas variáveis de ambiente!"
    echo ""
fi

echo "🐳 Iniciando containers Docker..."
docker-compose up --build -d mongodb qdrant ollama

echo "⏳ Aguardando serviços ficarem prontos..."
sleep 10

echo "🤖 Baixando modelo Ollama (qwen3-embedding)..."
docker-compose exec -T ollama ollama pull qwen3-embedding:0.6b

echo "📚 Carregando e indexando documentos..."
docker-compose up --build document-loader

echo "🎨 Iniciando aplicação Streamlit..."
docker-compose up --build -d streamlit-app

echo ""
echo "✅ Sistema iniciado com sucesso!"
echo ""
echo "📊 Acesse os serviços:"
echo "   🎨 Streamlit App: http://localhost:8501"
echo "   📊 Mongo Express: http://localhost:8081"
echo "   🔍 Qdrant Dashboard: http://localhost:6333/dashboard"
echo ""
echo "💡 Para ver os logs: docker-compose logs -f"
echo "🛑 Para parar: docker-compose down"
