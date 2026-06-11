#!/bin/bash
# Script para executar o projeto localmente

echo "╔════════════════════════════════════════════════════════════╗"
echo "║         VISCONDE - Organizador de Salas de Prova           ║"
echo "║                    Executar Localmente                      ║"
echo "╚════════════════════════════════════════════════════════════╝"

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não está instalado"
    exit 1
fi

echo "✅ Python encontrado"

# Criar ambiente virtual se não existir
if [ ! -d "venv" ]; then
    echo ""
    echo "📦 Criando ambiente virtual..."
    python3 -m venv venv
fi

# Ativar ambiente virtual
echo ""
echo "🔌 Ativando ambiente virtual..."
source venv/bin/activate

# Instalar dependências
echo ""
echo "📥 Instalando dependências..."
pip install -q -r requirements.txt

# Executar servidor
echo ""
echo "🚀 Iniciando servidor..."
echo ""
echo "   🌐 Acesse em: http://localhost:8000"
echo "   📚 Docs em:   http://localhost:8000/docs"
echo ""
echo "   Pressione Ctrl+C para parar"
echo ""

python api/index.py
