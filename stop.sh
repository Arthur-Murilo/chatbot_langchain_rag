#!/bin/bash

echo "🛑 Parando todos os serviços..."
docker-compose down

echo "🗑️  Removendo volumes (dados persistentes)..."
docker-compose down -v

echo "🧹 Limpando imagens não utilizadas..."
docker system prune -f

echo "✅ Cleanup concluído!"
