"""
Script de teste rápido para verificar integração frontend-backend
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_login():
    """Testa login e retorna token"""
    print("🔐 Testando login...")
    response = requests.post(
        f"{BASE_URL}/auth/login",
        data={
            "username": "admin@example.com",
            "password": "admin123"
        }
    )
    if response.status_code == 200:
        token = response.json()["access_token"]
        print("✅ Login bem-sucedido!")
        return token
    else:
        print(f"❌ Erro no login: {response.status_code}")
        print(response.json())
        return None

def test_search(token):
    """Testa busca semântica"""
    print("\n🔍 Testando busca semântica...")
    response = requests.post(
        f"{BASE_URL}/search/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "query": "teste",
            "top_k": 2
        }
    )
    if response.status_code == 200:
        data = response.json()
        print("✅ Busca bem-sucedida!")
        print(f"   Query: {data['query']}")
        print(f"   Total de resultados: {data['total_results']}")
        if data['results']:
            print(f"   Primeiro resultado: {data['results'][0]['document_name']}")
            print(f"   Similarity: {data['results'][0]['similarity_score']:.4f}")
        return True
    else:
        print(f"❌ Erro na busca: {response.status_code}")
        print(response.json())
        return False

def test_chat(token):
    """Testa chat com LLM"""
    print("\n💬 Testando chat...")
    response = requests.post(
        f"{BASE_URL}/chat/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "query": "qual o conteúdo do documento?",
            "use_context": True,
            "max_context_chunks": 2
        }
    )
    if response.status_code == 200:
        data = response.json()
        print("✅ Chat bem-sucedido!")
        print(f"   Query: {data['query']}")

        # VERIFICAÇÃO IMPORTANTE: Campo renomeado
        if 'llm_provider' in data:
            print(f"   ✅ Campo 'llm_provider' presente: {data['llm_provider']}")
        else:
            print(f"   ❌ Campo 'llm_provider' ausente!")

        if 'model_used' in data:
            print(f"   ⚠️  Campo antigo 'model_used' ainda presente!")

        print(f"   Contexto usado: {len(data['context_used'])} chunks")
        print(f"   Resposta: {data['answer'][:100]}...")
        return True
    else:
        print(f"❌ Erro no chat: {response.status_code}")
        print(response.json())
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("TESTE DE INTEGRAÇÃO FRONTEND-BACKEND")
    print("=" * 60)

    token = test_login()
    if token:
        test_search(token)
        test_chat(token)

    print("\n" + "=" * 60)
    print("TESTES CONCLUÍDOS!")
    print("=" * 60)
