"""
Script de teste local da API
Execute com: python test_api.py
"""

import requests
import sys
from pathlib import Path

BASE_URL = "http://localhost:8000"

def test_health():
    """Testa endpoint de health check"""
    print("🔍 Testando /api/health...")
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        assert response.status_code == 200, f"Status {response.status_code}"
        data = response.json()
        assert data["status"] == "ok", "Status não é 'ok'"
        print("✅ Health check passou!")
        return True
    except Exception as e:
        print(f"❌ Health check falhou: {e}")
        return False

def test_template_download():
    """Testa download do template"""
    print("\n🔍 Testando /api/template...")
    try:
        response = requests.get(f"{BASE_URL}/api/template")
        assert response.status_code == 200, f"Status {response.status_code}"
        assert len(response.content) > 0, "Arquivo vazio"
        assert response.headers.get('content-type') == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        print("✅ Template download passou!")
        return True
    except Exception as e:
        print(f"❌ Template download falhou: {e}")
        return False

def test_process():
    """Testa processamento de arquivo"""
    print("\n🔍 Testando /api/process...")
    try:
        # Usar arquivo de teste
        test_file = Path(__file__).parent / "data" / "alunos-fake.xlsx"
        if not test_file.exists():
            print(f"❌ Arquivo de teste não encontrado: {test_file}")
            return False
        
        with open(test_file, 'rb') as f:
            files = {'file': f}
            response = requests.post(f"{BASE_URL}/api/process", files=files)
        
        assert response.status_code == 200, f"Status {response.status_code}: {response.text}"
        data = response.json()
        assert data["status"] == "success", "Status não é 'success'"
        assert "session_id" in data, "Sem session_id"
        assert "stats" in data, "Sem stats"
        print(f"✅ Process passou!")
        print(f"   Session ID: {data['session_id']}")
        print(f"   Stats: {data['stats']}")
        return data["session_id"]
    except Exception as e:
        print(f"❌ Process falhou: {e}")
        return None

def test_download(session_id):
    """Testa download do resultado"""
    print(f"\n🔍 Testando /api/download/{session_id}...")
    try:
        response = requests.get(f"{BASE_URL}/api/download/{session_id}")
        assert response.status_code == 200, f"Status {response.status_code}"
        assert len(response.content) > 0, "Arquivo vazio"
        print("✅ Download passou!")
        return True
    except Exception as e:
        print(f"❌ Download falhou: {e}")
        return False

def test_stats(session_id):
    """Testa obtenção de stats"""
    print(f"\n🔍 Testando /api/stats/{session_id}...")
    try:
        response = requests.get(f"{BASE_URL}/api/stats/{session_id}")
        assert response.status_code == 200, f"Status {response.status_code}"
        data = response.json()
        assert data["status"] == "success", "Status não é 'success'"
        assert "stats" in data, "Sem stats"
        print(f"✅ Stats passou!")
        print(f"   Stats: {data['stats']}")
        return True
    except Exception as e:
        print(f"❌ Stats falhou: {e}")
        return False

def test_frontend():
    """Testa se frontend é servido"""
    print("\n🔍 Testando GET /...")
    try:
        response = requests.get(f"{BASE_URL}/")
        assert response.status_code == 200, f"Status {response.status_code}"
        assert "<!DOCTYPE html>" in response.text or "<html" in response.text, "HTML não encontrado"
        print("✅ Frontend sendo servido!")
        return True
    except Exception as e:
        print(f"❌ Frontend não encontrado: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("TESTE DA API - VISCONDE")
    print("=" * 60)
    
    results = []
    
    # Testes básicos
    results.append(("Health Check", test_health()))
    results.append(("Template Download", test_template_download()))
    results.append(("Frontend", test_frontend()))
    
    # Testes de processamento
    session_id = test_process()
    results.append(("Process", session_id is not None))
    
    if session_id:
        results.append(("Download", test_download(session_id)))
        results.append(("Stats", test_stats(session_id)))
    
    # Resumo
    print("\n" + "=" * 60)
    print("RESUMO DOS TESTES")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for test_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{test_name:.<40} {status}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print("=" * 60)
    print(f"Total: {passed} passaram, {failed} falharam")
    print("=" * 60)
    
    sys.exit(0 if failed == 0 else 1)
