# Quick Start Guide

Guia rápido para iniciar o projeto Document AI API.

## Início Rápido com Docker (Recomendado)

```bash
# 1. Configure as variáveis de ambiente
cp .env.example .env

# 2. Inicie os containers
docker-compose up -d

# 3. Acompanhe os logs
docker-compose logs -f app

# 4. Acesse a API
# http://localhost:8000/docs
```

Pronto! A API estará rodando em http://localhost:8000

## Primeiro Uso

### 1. Registrar usuário

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "teste@example.com",
    "username": "teste",
    "password": "senha123"
  }'
```

Ou use o usuário admin padrão:
- Email: `admin@example.com`
- Senha: `admin123`

### 2. Fazer login

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"
```

Salve o token retornado.

### 3. Upload de documento

```bash
TOKEN="seu-token-aqui"

curl -X POST "http://localhost:8000/api/v1/documents/upload" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@documento.pdf"
```

### 4. Buscar documentos

```bash
curl -X POST "http://localhost:8000/api/v1/search/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "contratos públicos",
    "top_k": 5
  }'
```

## Comandos Úteis

### Docker

```bash
# Parar containers
docker-compose down

# Parar e remover volumes (APAGA DADOS!)
docker-compose down -v

# Reconstruir imagens
docker-compose build --no-cache

# Ver logs
docker-compose logs -f

# Executar comando no container
docker-compose exec app bash

# Ver status
docker-compose ps
```

### Alembic (Migrations)

```bash
# Dentro do container ou ambiente local

# Ver status atual
alembic current

# Ver histórico
alembic history

# Criar nova migration
alembic revision --autogenerate -m "Descrição"

# Aplicar migrations
alembic upgrade head

# Reverter última migration
alembic downgrade -1
```

### Desenvolvimento Local (sem Docker)

```bash
# 1. Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Configurar .env
cp .env.example .env
# Editar DATABASE_URL para apontar para seu PostgreSQL local

# 4. Rodar migrations
alembic upgrade head

# 5. Criar admin
python setup_db.py

# 6. Iniciar servidor
uvicorn app.main:app --reload
```

## Troubleshooting Rápido

### Erro: "Connection refused"
```bash
# Verificar se containers estão rodando
docker-compose ps

# Reiniciar containers
docker-compose restart
```

### Erro: "Extension 'vector' does not exist"
```bash
# Conectar no PostgreSQL
docker-compose exec postgres psql -U user -d document_ai_db

# Criar extensão
CREATE EXTENSION vector;
```

### Erro: "Unauthorized"
```bash
# Verificar se o token está correto
# Fazer novo login para obter token válido
```

### Resetar banco de dados (CUIDADO!)
```bash
# Parar containers e remover volumes
docker-compose down -v

# Iniciar novamente (será criado do zero)
docker-compose up -d
```

## Integração LLM (Opcional)

### Ollama (Local)

```bash
# 1. Instalar Ollama
# https://ollama.ai

# 2. Baixar modelo
ollama pull llama2

# 3. Configurar .env
OLLAMA_BASE_URL=http://host.docker.internal:11434
OLLAMA_MODEL=llama2

# 4. Testar chat
curl -X POST "http://localhost:8000/api/v1/chat/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Resuma os documentos sobre licitações",
    "use_context": true
  }'
```

## Endpoints Principais

- **Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health**: http://localhost:8000/health

## Links Úteis

- [README completo](README.md) - Documentação completa
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Alembic Docs](https://alembic.sqlalchemy.org/)
- [pgvector](https://github.com/pgvector/pgvector)

## Suporte

Para dúvidas ou problemas:
1. Consulte o [README.md](README.md) completo
2. Verifique os logs: `docker-compose logs -f`
3. Verifique as issues no GitHub

---

Desenvolvido para o desafio técnico TCMRio
