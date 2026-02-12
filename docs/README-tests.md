# 🧪 Guia de Testes - Personal Trainer AI

## 📋 Visão Geral

Este projeto implementa uma **cultura de testes robusta** com diferentes níveis de testes para garantir qualidade, confiabilidade e facilitar manutenção.

---

## 🏗️ Estrutura de Testes

```
tests/
├── __init__.py              # Pacote de testes
├── conftest.py              # Fixtures compartilhadas
├── test_config.py           # Testes de configuração
├── test_loaders.py          # Testes de carregamento de docs
├── test_agents.py           # Testes do agente RAG
└── test_integration.py      # Testes de integração e E2E
```

---

## 🎯 Tipos de Testes

### 1. **Testes Unitários** (`@pytest.mark.unit`)

Testam componentes isolados sem dependências externas.

**Características:**
- ✅ Rápidos (< 100ms cada)
- ✅ Não requerem serviços externos
- ✅ Usam mocks para dependências
- ✅ Focados em lógica de negócio

**Exemplos:**
```bash
# Executar apenas testes unitários
./run_tests.sh -u

# Ou
pytest -m unit
```

**Arquivos:**
- `test_config.py`: Validação de configurações
- `test_agents.py`: Lógica do agente
- `test_loaders.py`: Processamento de documentos

---

### 2. **Testes de Integração** (`@pytest.mark.integration`)

Testam integração entre componentes e serviços.

**Características:**
- 🔄 Médios (~1-5s cada)
- 🔌 Requerem serviços rodando
- 📊 Verificam conectividade
- 🔍 Testam fluxos completos

**Exemplos:**
```bash
# Executar apenas testes de integração
./run_tests.sh -i

# Ou
pytest -m integration
```

**Arquivos:**
- `test_integration.py`: Conectividade de serviços

---

### 3. **Testes End-to-End** (`@pytest.mark.slow`)

Testam fluxos completos do sistema.

**Características:**
- 🐌 Lentos (> 5s cada)
- 🌐 Requerem todos os serviços
- 🎯 Simulam uso real
- 🔐 Testam requisitos críticos

**Exemplos:**
```bash
# Executar testes E2E
pytest -m slow -v
```

---

## 🚀 Como Executar os Testes

### Método 1: Script Automatizado (Recomendado)

```bash
# Dar permissão de execução (primeira vez)
chmod +x run_tests.sh

# Todos os testes
./run_tests.sh

# Apenas unitários
./run_tests.sh -u

# Apenas integração
./run_tests.sh -i

# Rápidos (sem integração/slow)
./run_tests.sh -f

# Com cobertura de código
./run_tests.sh -c

# Modo verboso
./run_tests.sh -v

# Combinações
./run_tests.sh -u -c -v  # Unitários + cobertura + verboso
```

### Método 2: Pytest Direto

```bash
# Todos os testes
pytest tests/

# Com output verboso
pytest tests/ -v

# Testes específicos
pytest tests/test_config.py

# Por marcador
pytest -m unit
pytest -m integration

# Parar no primeiro erro
pytest tests/ -x

# Com cobertura
pytest tests/ --cov=src --cov-report=html
```

---

## 📊 Relatório de Cobertura

### Gerar Relatório

```bash
# Via script
./run_tests.sh -c

# Via pytest
pytest tests/ --cov=src --cov-report=html --cov-report=term
```

### Visualizar Relatório

```bash
# Abrir no navegador
firefox htmlcov/index.html
# ou
google-chrome htmlcov/index.html
```

### Meta de Cobertura

| Componente | Meta | Atual |
|------------|------|-------|
| Config | 90%+ | - |
| Loaders | 80%+ | - |
| Agents | 85%+ | - |
| Interface | 70%+ | - |
| **Geral** | **80%+** | - |

---

## 🔧 Configuração de Testes

### Instalar Dependências

```bash
pip install -r requirements-test.txt
```

### Variáveis de Ambiente

Testes usam as mesmas variáveis do `.env`:

```bash
# Copiar exemplo
cp .env.example .env

# Editar com suas configurações
nano .env
```

### Fixtures Compartilhadas

Em `conftest.py`:

```python
@pytest.fixture
def mock_settings():
    """Mock de configurações para teste"""
    ...

@pytest.fixture
def sample_documents():
    """Documentos de exemplo"""
    ...
```

---

## 🎯 Casos de Teste Críticos

### 1. Conectividade de Serviços

```python
def test_qdrant_health():
    """Verifica se Qdrant está online"""
    response = requests.get("http://localhost:6333/healthz")
    assert response.status_code == 200
```

### 2. Processamento de Documentos

```python
def test_carregar_documentos():
    """Verifica carregamento de documentos"""
    docs = carregar_documentos("data/")
    assert len(docs) > 0
```

### 3. Pipeline RAG

```python
def test_complete_rag_query():
    """Testa query completa do RAG"""
    agent = PersonalTrainerAgent(session_id="test")
    response = agent.query("O que é hipertrofia?")
    assert response is not None
    assert len(response) > 10
```

### 4. Histórico de Conversa

```python
def test_chat_history():
    """Verifica persistência de histórico"""
    agent = PersonalTrainerAgent(session_id="test")
    agent.query("Teste")
    history = agent.get_chat_history()
    assert len(history) > 0
```

---

## 🐛 Troubleshooting

### Erro: Services Not Running

```
❌ Qdrant não está rodando
```

**Solução:**
```bash
# Iniciar serviços
docker-compose up -d

# Verificar status
docker-compose ps

# Ver logs
docker-compose logs qdrant
```

### Erro: Module Not Found

```
ModuleNotFoundError: No module named 'pytest'
```

**Solução:**
```bash
pip install -r requirements-test.txt
```

### Erro: Collection Not Found

```
⚠️ Collection está vazia
```

**Solução:**
```bash
# Executar loader
python src/loaders/document_loader.py

# Ou via Docker
docker-compose run document-loader
```

### Erro: API Key Invalid

```
❌ GROQ_API_KEY inválida
```

**Solução:**
```bash
# Verificar .env
cat .env | grep GROQ_API_KEY

# Obter nova chave em: https://console.groq.com/
```

---

## 📈 Dashboard de Saúde do Sistema

Execute o health check:

```bash
pytest tests/test_integration.py::test_system_health_report -v
```

**Output esperado:**
```
📊 RELATÓRIO DE SAÚDE DO SISTEMA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Qdrant          ✅ Online
Ollama          ✅ Online
MongoDB         ✅ Online
Streamlit       ✅ Online
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Todos os 4 serviços estão online!
```

---

## 🔄 CI/CD (Futuro)

### GitHub Actions

```yaml
# .github/workflows/tests.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-test.txt
      - name: Run tests
        run: pytest tests/ --cov=src
```

---

## 📚 Boas Práticas

### 1. **Escrever Testes Primeiro** (TDD)

```python
# 1. Escrever teste que falha
def test_new_feature():
    result = new_feature()
    assert result == expected

# 2. Implementar feature
def new_feature():
    return expected

# 3. Refatorar
```

### 2. **Usar Fixtures**

```python
@pytest.fixture
def sample_data():
    return {"key": "value"}

def test_with_fixture(sample_data):
    assert sample_data["key"] == "value"
```

### 3. **Nomear Testes Claramente**

```python
# ❌ Ruim
def test_1():
    ...

# ✅ Bom
def test_agent_returns_valid_response():
    ...
```

### 4. **Testar Edge Cases**

```python
def test_empty_input():
    result = function("")
    assert result is None

def test_invalid_input():
    with pytest.raises(ValueError):
        function(invalid_input)
```

### 5. **Manter Testes Rápidos**

```python
# Use mocks para operações lentas
@patch('src.agents.agent.ChatGroq')
def test_fast(mock_groq):
    mock_groq.return_value = Mock()
    # Teste rápido sem chamada real à API
```

---

## 📝 Checklist de Testes

Antes de fazer commit:

- [ ] Todos os testes passam: `./run_tests.sh`
- [ ] Cobertura > 80%: `./run_tests.sh -c`
- [ ] Testes unitários rápidos (< 5s total)
- [ ] Serviços críticos testados
- [ ] Novos códigos têm testes
- [ ] Documentação atualizada

---

## 🚀 Próximos Passos

- [ ] Adicionar testes de performance
- [ ] Implementar testes de carga
- [ ] Adicionar testes de segurança
- [ ] Configurar CI/CD
- [ ] Adicionar mutation testing
- [ ] Implementar testes de regressão visual

---

## 📞 Suporte

Problemas com testes?

- 📖 Revise este guia
- 🐛 Abra uma issue no GitHub
- 💬 Consulte a documentação do pytest

---

**Última atualização**: 11 de fevereiro de 2026  
**Mantido por**: Arthur Murilo
