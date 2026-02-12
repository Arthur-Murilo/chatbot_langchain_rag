# 🤖 Documentação - Agentes RAG

## 📋 Visão Geral

O módulo `agents` é o coração do sistema Personal Trainer AI, implementando a lógica de **Retrieval-Augmented Generation (RAG)** usando LangChain. Este componente orquestra a busca semântica e geração de respostas contextualizadas.

---

## 📁 Estrutura

```
src/agents/
├── __init__.py
└── agent.py          # Implementação principal do agente RAG
```

---

## 🔧 Componente Principal: `agent.py`

### Classe `PersonalTrainerAgent`

Gerencia todo o pipeline RAG, desde a recuperação de documentos até a geração de respostas.

#### Atributos Principais

```python
self.llm: ChatGroq                    # Modelo de linguagem (Groq)
self.embeddings: OllamaEmbeddings     # Gerador de embeddings (Ollama)
self.vector_store: Qdrant             # Base vetorial (Qdrant)
self.chat_history: ChatMessageHistory # Histórico da conversa (MongoDB)
self.memory: ConversationBufferMemory # Memória de contexto
```

#### Métodos Principais

##### `__init__(session_id: str)`

Inicializa o agente com todas as dependências necessárias.

**Parâmetros:**
- `session_id` (str): Identificador único da sessão do usuário

**Exemplo:**
```python
agent = PersonalTrainerAgent(session_id="user_123")
```

**O que faz:**
1. Configura conexão com Groq LLM
2. Inicializa embeddings Ollama
3. Conecta ao Qdrant para busca vetorial
4. Configura histórico persistente no MongoDB
5. Cria chain RAG com retrieval

---

##### `query(question: str) -> str`

Processa uma pergunta e retorna resposta contextualizada.

**Parâmetros:**
- `question` (str): Pergunta do usuário

**Retorno:**
- `str`: Resposta gerada pelo LLM com contexto recuperado

**Fluxo de Execução:**
```
Pergunta → Embedding → Busca Qdrant → Top-3 Docs → LLM → Resposta
```

**Exemplo:**
```python
resposta = agent.query("Como fazer agachamento corretamente?")
print(resposta)
```

---

##### `get_chat_history() -> List[Dict]`

Recupera todo o histórico de conversa da sessão.

**Retorno:**
- `List[Dict]`: Lista de mensagens com formato `{"role": "user/assistant", "content": "..."}`

**Exemplo:**
```python
historico = agent.get_chat_history()
for msg in historico:
    print(f"{msg['role']}: {msg['content']}")
```

---

##### `clear_history()`

Limpa todo o histórico da sessão atual.

**Exemplo:**
```python
agent.clear_history()
print("Histórico apagado!")
```

---

## 🔄 Fluxo de Dados Detalhado

### 1. Inicialização do Agente

```mermaid
graph TD
    A[Criar PersonalTrainerAgent] --> B[Conectar Groq LLM]
    B --> C[Inicializar Ollama Embeddings]
    C --> D[Conectar Qdrant]
    D --> E[Configurar MongoDB History]
    E --> F[Criar RAG Chain]
    F --> G[Agente Pronto]
```

### 2. Processamento de Query

```mermaid
sequenceDiagram
    participant U as Usuário
    participant A as Agent
    participant E as Embeddings
    participant Q as Qdrant
    participant L as LLM
    participant M as MongoDB
    
    U->>A: query("Como fazer flexão?")
    A->>E: Gerar embedding da pergunta
    E-->>A: Vector [768 dims]
    A->>Q: Buscar documentos similares
    Q-->>A: Top-3 documentos relevantes
    A->>L: Pergunta + Contexto + Histórico
    L-->>A: Resposta gerada
    A->>M: Salvar pergunta e resposta
    A-->>U: Retornar resposta
```

---

## 🧩 Componentes Integrados

### 1. **LLM - Groq (ChatGroq)**

**Configuração:**
```python
llm = ChatGroq(
    groq_api_key=settings.GROQ_API_KEY,
    model_name=settings.LLM_MODEL,
    temperature=settings.LLM_TEMPERATURE,
    max_tokens=settings.LLM_MAX_TOKENS
)
```

**Modelos Suportados:**
- `openai/gpt-oss-120b` (padrão, recomendado)
- `llama-3.3-70b-versatile`
- `mixtral-8x7b-32768`

**Responsabilidades:**
- Gerar respostas naturais e contextualizadas
- Interpretar contexto recuperado
- Manter coerência com histórico

---

### 2. **Embeddings - Ollama**

**Configuração:**
```python
embeddings = OllamaEmbeddings(
    model=settings.OLLAMA_MODEL,
    base_url=settings.OLLAMA_BASE_URL
)
```

**Modelo Usado:**
- `qwen3-embedding:0.6b` (768 dimensões)

**Responsabilidades:**
- Converter texto em vetores numéricos
- Garantir consistência semântica
- Otimizar para busca vetorial

---

### 3. **Vector Store - Qdrant**

**Configuração:**
```python
vector_store = Qdrant(
    client=QdrantClient(url=settings.QDRANT_URL),
    collection_name=settings.QDRANT_COLLECTION,
    embeddings=embeddings
)
```

**Responsabilidades:**
- Armazenar embeddings dos documentos
- Realizar busca por similaridade (cosine similarity)
- Retornar top-K documentos mais relevantes (K=3)

---

### 4. **Memória - MongoDB**

**Configuração:**
```python
chat_history = MongoDBChatMessageHistory(
    connection_string=settings.get_mongo_uri(),
    database_name=settings.MONGO_DATABASE,
    collection_name=settings.MONGO_COLLECTION,
    session_id=session_id
)
```

**Responsabilidades:**
- Persistir histórico de conversas
- Carregar contexto de sessões anteriores
- Permitir continuidade entre sessões

---

## ⚙️ Configurações

### Variáveis de Ambiente Utilizadas

```bash
# LLM
GROQ_API_KEY=gsk_...
LLM_MODEL=openai/gpt-oss-120b
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=1000

# Embeddings
OLLAMA_MODEL=qwen3-embedding:0.6b
OLLAMA_BASE_URL=http://localhost:11434

# Vector Store
QDRANT_URL=http://localhost:6333
QDRANT_COLLECTION=rag_gym_personal

# Memória
MONGO_URI=mongodb://user:pass@host:port
MONGO_DATABASE=chat_history
MONGO_COLLECTION=message_store
```

---

## 🎯 Casos de Uso

### 1. Resposta Simples

```python
from src.agents.agent import PersonalTrainerAgent

agent = PersonalTrainerAgent(session_id="user_123")
resposta = agent.query("O que é hipertrofia?")
print(resposta)
```

### 2. Conversa Multi-turno

```python
agent = PersonalTrainerAgent(session_id="user_123")

# Pergunta 1
r1 = agent.query("Como fazer agachamento?")
print(r1)

# Pergunta 2 (com contexto da anterior)
r2 = agent.query("Quantas séries devo fazer?")
print(r2)

# Pergunta 3
r3 = agent.query("E para iniciantes?")
print(r3)
```

### 3. Gerenciamento de Histórico

```python
agent = PersonalTrainerAgent(session_id="user_123")

# Ver histórico
historico = agent.get_chat_history()
print(f"Total de mensagens: {len(historico)}")

# Limpar histórico
agent.clear_history()
print("Histórico limpo!")
```

---

## 🔍 Retrieval Strategy

### Parâmetros de Busca

```python
retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}  # Top-3 documentos
)
```

**Estratégia:**
- **Tipo**: Similarity Search (Cosine)
- **Top-K**: 3 documentos mais relevantes
- **Score Threshold**: Não definido (retorna sempre top-3)

### Como Funciona

1. Pergunta do usuário é convertida em embedding (768d)
2. Qdrant calcula similaridade cosseno com todos os documentos
3. Retorna os 3 documentos com maior score
4. Documentos são concatenados e enviados ao LLM

---

## 🧪 Prompts do Sistema

Os prompts são definidos em `src/config/prompts.py`:

```python
SYSTEM_PROMPT = """
Você é um personal trainer especializado em musculação e fitness.
Use o contexto fornecido para responder as perguntas de forma precisa.
Se não souber a resposta, seja honesto e diga que não tem certeza.
"""
```

**Características:**
- Define o papel do assistente
- Instrui a usar contexto recuperado
- Orienta sobre honestidade em respostas

---

## 📊 Performance

### Métricas Típicas

| Métrica | Valor |
|---------|-------|
| Tempo de embedding | ~50-100ms |
| Busca vetorial | ~20-50ms |
| Geração LLM | ~1-3s |
| **Total por query** | **~1.5-4s** |

### Otimizações

- ✅ Embeddings locais (Ollama) para baixa latência
- ✅ Qdrant com índice HNSW para busca rápida
- ✅ Groq com LPUs para inferência rápida
- ✅ Cache de histórico no MongoDB

---

## 🐛 Troubleshooting

### Erro: `Connection refused to Qdrant`

```bash
# Verificar se Qdrant está rodando
docker-compose ps qdrant

# Reiniciar se necessário
docker-compose restart qdrant
```

### Erro: `Invalid GROQ_API_KEY`

```bash
# Verificar variável de ambiente
echo $GROQ_API_KEY

# Ou no .env
cat .env | grep GROQ_API_KEY
```

### Erro: `No documents found in collection`

```bash
# Executar o loader
python src/loaders/document_loader.py

# Ou via Docker
docker-compose run document-loader
```

---

## 📚 Referências

- [LangChain Documentation](https://python.langchain.com/)
- [Groq API Docs](https://console.groq.com/docs)
- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [Ollama Embeddings](https://ollama.ai/library/qwen3-embedding)

---

**Última atualização**: 11 de fevereiro de 2026
