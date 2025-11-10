# TCM SmartDocs - Desafio Técnico TCMRio

API de processamento e busca semântica em documentos jurídicos e técnicos, desenvolvida como parte do desafio técnico para a vaga de Desenvolvedor Pleno Python no TCMRio.

## Funcionalidades

- **Autenticação JWT** - Sistema seguro de login e controle de acesso
- **Upload de Documentos** - Suporte a PDF e DOCX com validação
- **Extração de Texto** - Processamento automático de documentos
- **Vetorização** - Embeddings com Sentence Transformers
- **Busca Semântica** - Busca vetorial inteligente com pgvector
- **Chat com LLM** - Perguntas sobre documentos usando LLM (ollama)
- **Logging Estruturado** - Logs em JSON para análise
- **Tratamento Global de Erros** - Middleware para erros padronizados

## Tecnologias Utilizadas

- **FastAPI** - Framework web
- **PostgreSQL + pgvector** - Banco de dados com suporte a vetores
- **SQLAlchemy** - ORM para Python
- **Alembic** - Migrations de banco de dados
- **Sentence Transformers** - Geração de embeddings (all-MiniLM-L6-v2)
- **PyJWT** - Autenticação JWT
- **Docker** - Containerização da aplicação
- **Pydantic** - Validação de dados

## Arquitetura

O projeto segue princípios de Clean Architecture e SOLID:

```
app/
├── api/              # Camada de apresentação (endpoints)
│   ├── v1/
│   │   └── endpoints/
│   └── dependencies.py
├── core/             # Configurações e utilitários centrais
│   ├── config.py
│   ├── security.py
│   ├── logging.py
│   └── exceptions.py
├── db/               # Configuração de banco de dados
├── models/           # Modelos SQLAlchemy
├── repositories/     # Camada de acesso a dados
├── schemas/          # Schemas Pydantic (DTOs)
├── services/         # Lógica de negócio
├── middleware/       # Middlewares customizados
└── utils/            # Utilitários (validação, extração, chunking)
```

## Pré-requisitos

- Docker e Docker Compose (recomendado)
- OU:
  - Python 3.11+
  - PostgreSQL 14+ com extensão pgvector

## Instalação e Execução

### Opção 1: Docker (Recomendado)

### 1. Configurar Banco de Dados PostgreSQL

```bash
cd document-ai-project/backend

# Iniciar PostgreSQL com Docker
docker-compose up -d postgres

# Aguardar banco inicializar (5-10 segundos)
timeout /t 10

# Ou no Linux/Mac:
# sleep 10
```

### 2. Configurar Ambiente Python

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente (Windows)
venv\Scripts\activate
# ou
source venv/Scripts/activate

# Ou Linux/Mac:
# source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### 3. Inicializar Banco de Dados

```bash
# Rodar script de setup (cria extensão pgvector, tabelas e usuário admin)
python setup_db.py
```

### 4. Iniciar Backend

```bash
# Rodar servidor
uvicorn app.main:app --reload

# Backend estará em: http://localhost:8000
# Documentação (Swagger): http://localhost:8000/docs
```

### Opção 2: Execução Local

1. **Instale o PostgreSQL com pgvector**

```bash
# Ubuntu/Debian
sudo apt install postgresql postgresql-contrib
# Instale pgvector: https://github.com/pgvector/pgvector
```

2. **Crie um ambiente virtual Python**

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
# ou
source venv/Scripts/activate
```

3. **Instale as dependências**

```bash
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente**

```bash
cp .env.example .env
# Edite .env com suas configurações
```

5. **Execute as migrations do banco de dados**

```bash
alembic upgrade head
```

6. **Inicie a aplicação**

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Configuração

### Variáveis de Ambiente Principais

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/document_ai_db

# Security
SECRET_KEY=sua-chave-secreta-muito-segura-aqui
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application
UPLOAD_DIR=./uploads
MAX_FILE_SIZE_MB=10

# Vector
EMBEDDING_MODEL=all-MiniLM-L6-v2
VECTOR_DIMENSION=384

# LLM (Opcional - escolha um)
OPENAI_API_KEY=sk-your-key
# ou
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2

# N8n (Opcional)
N8N_WEBHOOK_URL=http://localhost:5678/webhook/document-upload
```

Consulte `.env.example` para todas as opções disponíveis.

## Uso da API

### 1. Registrar Usuário

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "usuario@example.com",
    "username": "usuario",
    "password": "senha123"
  }'
```

### 2. Login

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=usuario&password=senha123"
```

Resposta:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Upload de Documento

```bash
curl -X POST "http://localhost:8000/api/v1/documents/upload" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -F "file=@/caminho/para/documento.pdf"
```

### 4. Busca Semântica

```bash
curl -X POST "http://localhost:8000/api/v1/search/" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "O que diz sobre contratos públicos?",
    "top_k": 5
  }'
```

### 5. Chat com LLM (se configurado)

```bash
curl -X POST "http://localhost:8000/api/v1/chat/" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Resuma os principais pontos sobre licitações",
    "use_context": true,
    "max_context_chunks": 5
  }'
```

## Documentação da API

Após iniciar a aplicação, acesse:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Integração com LLM (Opcional)

### OpenAI

1. Obtenha uma API key em https://platform.openai.com
2. Configure no `.env`:
   ```env
   OPENAI_API_KEY=sk-your-key-here
   ```
3. Descomente a integração em `app/services/llm_service.py:88-126`

### Ollama (Local)

1. Instale Ollama: https://ollama.ai
2. Baixe um modelo:
   ```bash
   ollama pull llama2 ou outro modelo mais leve
   ```
3. Configure no `.env`:
   ```env
   OLLAMA_BASE_URL=http://localhost:11434
   OLLAMA_MODEL=llama2
   ```

## Integração com N8n (Opcional)

1. Instale N8n: https://n8n.io
2. Crie um workflow com Webhook trigger
3. Configure a URL no `.env`:
   ```env
   N8N_WEBHOOK_URL=http://localhost:5678/webhook/document-upload
   ```
4. Descomente a notificação em `app/services/document_service.py:102`
5. Implemente o método seguindo o exemplo em `app/services/document_service.py:113-167`

## Banco de Dados

### Migrations com Alembic

Criar nova migration:
```bash
alembic revision --autogenerate -m "Descrição da mudança"
```

Aplicar migrations:
```bash
alembic upgrade head
```

Reverter última migration:
```bash
alembic downgrade -1
```

Ver histórico:
```bash
alembic history
```

### Usuário Admin Padrão

Ao executar pela primeira vez, um usuário admin é criado:
- **Email**: admin@example.com
- **Senha**: admin123

**IMPORTANTE**: Altere a senha em produção!

## Estrutura do Banco de Dados

### Tabelas Principais

- **users** - Usuários do sistema
- **documents** - Metadados dos documentos
- **vector_store** - Embeddings vetoriais dos chunks (com pgvector)

### Relacionamentos

- User 1:N Documents
- Document 1:N VectorStore (cascade delete)

## Testes

```bash
# Executar todos os testes
pytest

# Com coverage
pytest --cov=app --cov-report=html

# Testes específicos
pytest tests/test_auth.py
```

## Logging

Logs estruturados em JSON (configurável em `.env`):

```json
{
  "timestamp": "2025-11-10T00:00:00",
  "level": "INFO",
  "logger": "app.services.document_service",
  "message": "Documento criado no banco: ID 123",
  "module": "document_service",
  "function": "upload_document"
}
```

Configurações:
- `LOG_LEVEL`: DEBUG, INFO, WARNING, ERROR
- `LOG_FORMAT`: json ou text

## Segurança

### Implementações

- Autenticação JWT com expiração configurável
- Hash de senhas com bcrypt
- Validação de tipos e tamanhos de arquivo
- Geração de nomes de arquivo seguros (UUID)
- Verificação de proprietário em operações
- Rate limiting (via middleware - pode ser adicionado)

### Boas Práticas

- Nunca commite o arquivo `.env`
- Use SECRET_KEY forte (mínimo 32 caracteres)
- Configure CORS adequadamente para produção
- Mantenha dependências atualizadas
- Use HTTPS em produção

## Troubleshooting

### Erro: "Extension 'vector' does not exist"

```bash
# Conecte no PostgreSQL e execute:
CREATE EXTENSION vector;
```

### Erro: "Connection refused" no Docker

```bash
# Verifique se os containers estão rodando:
docker-compose ps

# Veja os logs:
docker-compose logs -f app
```

### Erro: "Model download failed"

O modelo de embedding será baixado na primeira execução. Certifique-se de ter conexão com internet.

### Problemas com migrations

```bash
# Reset do banco (CUIDADO: apaga dados!)
alembic downgrade base
alembic upgrade head
```

## Decisões Técnicas

### Por que Sentence Transformers?

- Modelo leve (all-MiniLM-L6-v2: 80MB)
- Excelente custo-benefício
- Execução local (sem custos de API)
- Boa performance em português

### Por que Repository Pattern?

- Separação clara entre lógica de negócio e acesso a dados
- Facilita testes unitários
- Permite trocar implementação de persistência

### Por que pgvector?

- Integração nativa com PostgreSQL
- Performance excelente para busca vetorial
- Simplicidade (não precisa de banco vetorial separado)

## Melhorias Futuras

- [ ] Testes unitários e de integração completos
- [ ] Rate limiting por usuário
- [ ] Suporte a mais formatos (TXT, RTF, etc)
- [ ] OCR para PDFs escaneados
- [ ] Cache de embeddings
- [ ] Paginação otimizada para grandes volumes
- [ ] Webhooks para eventos
- [ ] Monitoramento com Prometheus/Grafana
- [ ] CI/CD com GitHub Actions

## Contribuindo

1. Faça fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

## Licença

Este projeto foi desenvolvido como parte de um desafio técnico.

## Autor

Desenvolvido por [Seu Nome] como parte do processo seletivo para Desenvolvedor Pleno Python no TCMRio.

## Contato

- Email: seu-email@example.com
- LinkedIn: seu-perfil
- GitHub: seu-usuario

---

**Nota**: Este projeto foi desenvolvido seguindo as especificações do desafio técnico do TCMRio. Algumas funcionalidades (LLM, N8n) são opcionais e estão preparadas para integração conforme documentado.
