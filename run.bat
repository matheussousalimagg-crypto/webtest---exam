@echo off
REM Script para executar o projeto localmente (Windows)

echo ════════════════════════════════════════════════════════════
echo          VISCONDE - Organizador de Salas de Prova
echo                    Executar Localmente
echo ════════════════════════════════════════════════════════════

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não está instalado ou não está no PATH
    pause
    exit /b 1
)

echo ✅ Python encontrado

REM Criar ambiente virtual se não existir
if not exist "venv" (
    echo.
    echo 📦 Criando ambiente virtual...
    python -m venv venv
)

REM Ativar ambiente virtual
echo.
echo 🔌 Ativando ambiente virtual...
call venv\Scripts\activate.bat

REM Instalar dependências
echo.
echo 📥 Instalando dependências...
pip install -q -r requirements.txt

REM Executar servidor
echo.
echo 🚀 Iniciando servidor...
echo.
echo    🌐 Acesse em: http://localhost:8000
echo    📚 Docs em:   http://localhost:8000/docs
echo.
echo    Pressione Ctrl+C para parar
echo.

python api/index.py
pause
