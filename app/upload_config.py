"""
Configuração e utilitários para upload de arquivos
"""

import os
import tempfile
import uuid
from pathlib import Path
from typing import Optional

# Diretório temporário para uploads
UPLOAD_DIR = Path(tempfile.gettempdir()) / "visconde_uploads"

# Criar diretório se não existir
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Configurações de upload
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
ALLOWED_EXTENSIONS = {'.xlsx', '.xls'}

def generate_session_id() -> str:
    """Gera um ID único para a sessão"""
    return str(uuid.uuid4())

def is_valid_file(filename: str) -> bool:
    """Valida se o arquivo tem extensão permitida"""
    ext = Path(filename).suffix.lower()
    return ext in ALLOWED_EXTENSIONS

def cleanup_old_uploads(days: int = 1) -> None:
    """Remove uploads antigos (older than specified days)"""
    import time
    import os
    
    now = time.time()
    cutoff = now - (days * 86400)
    
    try:
        for file in UPLOAD_DIR.glob("*"):
            if file.is_file() and os.stat(file).st_mtime < cutoff:
                file.unlink()
    except Exception as e:
        print(f"Erro ao limpar uploads antigos: {e}")

if __name__ == "__main__":
    print(f"Upload directory: {UPLOAD_DIR}")
    print(f"Max file size: {MAX_FILE_SIZE / 1024 / 1024} MB")
    print(f"Allowed extensions: {ALLOWED_EXTENSIONS}")
