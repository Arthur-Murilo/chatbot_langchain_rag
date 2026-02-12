#!/bin/bash

# ============================================================================
# Script de Execução de Testes - Personal Trainer AI
# ============================================================================
# 
# Este script executa todos os testes do projeto com diferentes níveis
# de verbosidade e relatórios.
#
# Uso:
#   ./run_tests.sh [opções]
#
# Opções:
#   -u, --unit          Executar apenas testes unitários
#   -i, --integration   Executar apenas testes de integração
#   -f, --fast          Executar testes rápidos (sem integração)
#   -c, --coverage      Gerar relatório de cobertura
#   -v, --verbose       Modo verboso
#   -h, --help          Exibir esta mensagem de ajuda
#
# ============================================================================

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
RUN_UNIT=true
RUN_INTEGRATION=true
COVERAGE=false
VERBOSE=""
PYTEST_ARGS=""

# Print banner
print_banner() {
    echo -e "${GREEN}╔════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║   🧪 Personal Trainer AI - Test Suite         ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════╝${NC}"
    echo ""
}

# Print section header
print_section() {
    echo -e "${BLUE}▶ $1${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

# Print success message
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

# Print error message
print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Print warning message
print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Show help
show_help() {
    echo "Uso: ./run_tests.sh [opções]"
    echo ""
    echo "Opções:"
    echo "  -u, --unit          Executar apenas testes unitários"
    echo "  -i, --integration   Executar apenas testes de integração"
    echo "  -f, --fast          Executar testes rápidos (sem integração/slow)"
    echo "  -c, --coverage      Gerar relatório de cobertura"
    echo "  -v, --verbose       Modo verboso"
    echo "  -h, --help          Exibir esta mensagem de ajuda"
    echo ""
    echo "Exemplos:"
    echo "  ./run_tests.sh                    # Todos os testes"
    echo "  ./run_tests.sh -u                 # Apenas unitários"
    echo "  ./run_tests.sh -i -v              # Integração verboso"
    echo "  ./run_tests.sh -f -c              # Rápidos com cobertura"
    exit 0
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -u|--unit)
            RUN_INTEGRATION=false
            PYTEST_ARGS="$PYTEST_ARGS -m unit"
            shift
            ;;
        -i|--integration)
            RUN_UNIT=false
            PYTEST_ARGS="$PYTEST_ARGS -m integration"
            shift
            ;;
        -f|--fast)
            PYTEST_ARGS="$PYTEST_ARGS -m 'not slow and not requires_services'"
            shift
            ;;
        -c|--coverage)
            COVERAGE=true
            shift
            ;;
        -v|--verbose)
            VERBOSE="-vv"
            shift
            ;;
        -h|--help)
            show_help
            ;;
        *)
            print_error "Opção desconhecida: $1"
            show_help
            ;;
    esac
done

# Main execution
main() {
    print_banner
    
    # Check if pytest is installed
    print_section "Verificando dependências"
    if ! command -v pytest &> /dev/null; then
        print_error "pytest não encontrado!"
        echo "Instale as dependências de teste:"
        echo "  pip install -r requirements-test.txt"
        exit 1
    fi
    print_success "pytest instalado"
    
    # Check if in project root
    if [ ! -f "requirements.txt" ]; then
        print_error "Execute este script da raiz do projeto"
        exit 1
    fi
    print_success "Diretório correto"
    echo ""
    
    # Run health check
    print_section "Verificando Saúde dos Serviços"
    pytest tests/test_integration.py::test_system_health_report -v --tb=no || true
    echo ""
    
    # Build pytest command
    PYTEST_CMD="pytest tests/"
    
    if [ "$COVERAGE" = true ]; then
        PYTEST_CMD="$PYTEST_CMD --cov=src --cov-report=html --cov-report=term-missing"
    fi
    
    PYTEST_CMD="$PYTEST_CMD $VERBOSE $PYTEST_ARGS"
    
    # Run tests
    print_section "Executando Testes"
    echo "Comando: $PYTEST_CMD"
    echo ""
    
    if $PYTEST_CMD; then
        echo ""
        print_success "Todos os testes passaram!"
        
        if [ "$COVERAGE" = true ]; then
            echo ""
            print_section "Relatório de Cobertura"
            echo "Relatório HTML gerado em: htmlcov/index.html"
            echo "Abra no navegador:"
            echo "  firefox htmlcov/index.html"
            echo "  ou"
            echo "  google-chrome htmlcov/index.html"
        fi
        
        exit 0
    else
        echo ""
        print_error "Alguns testes falharam!"
        echo ""
        print_warning "Dicas:"
        echo "  • Verifique se os serviços estão rodando: docker-compose ps"
        echo "  • Inicie os serviços: ./start.sh"
        echo "  • Execute testes específicos: pytest tests/test_config.py -v"
        echo "  • Use modo verboso para mais detalhes: ./run_tests.sh -v"
        exit 1
    fi
}

# Trap errors
trap 'print_error "Erro na linha $LINENO"' ERR

# Run main
main
