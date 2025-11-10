FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Atualizar pip
RUN pip install --upgrade pip

# Copiar requirements
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY ./app ./app
COPY .env .env
COPY setup_db.py .

# Copiar configuração do Alembic
COPY alembic.ini .
COPY ./alembic ./alembic

# Copiar script de inicialização
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# Criar diretório uploads
RUN mkdir -p uploads

# Expor porta
EXPOSE 8000

# Comando de inicialização
ENTRYPOINT ["./entrypoint.sh"]
