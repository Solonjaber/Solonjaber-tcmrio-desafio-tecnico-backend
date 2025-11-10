from typing import List, Optional
from app.schemas.search import SearchResult
from app.core.config import settings
from app.core.logging import logger
import httpx

class LLMService:
    """
    Service para integração com LLM

    🔧 VOCÊ INTEGRA: Escolha uma das opções e implemente

    Responsabilidades:
    - Gerar respostas usando LLM
    - Construir prompts com contexto
    - Gerenciar chamadas à API
    """

    def __init__(self):
        self.provider = self._detect_provider()
        logger.info(f"LLM Provider detectado: {self.provider}")

    def _detect_provider(self) -> str:
        """Detecta qual provider está configurado"""
        if settings.OPENAI_API_KEY:
            return "openai"
        elif settings.AZURE_OPENAI_API_KEY:
            return "azure"
        elif settings.OLLAMA_BASE_URL:
            return "ollama"
        else:
            return "none"

    async def generate_answer(
        self,
        query: str,
        context_chunks: List[SearchResult]
    ) -> str:
        """
        Gera resposta usando LLM baseado no contexto fornecido
        """

        if self.provider == "none":
            return self._fallback_answer(context_chunks)

        # 🔧 OPÇÃO 1: OpenAI
        if self.provider == "openai":
            return await self._generate_with_openai(query, context_chunks)

        # 🔧 OPÇÃO 2: Azure OpenAI
        elif self.provider == "azure":
            return await self._generate_with_azure(query, context_chunks)

        # 🔧 OPÇÃO 3: Ollama (local)
        elif self.provider == "ollama":
            return await self._generate_with_ollama(query, context_chunks)

    def _build_prompt(self, query: str, context_chunks: List[SearchResult]) -> str:
        """Constrói prompt com contexto"""
        if not context_chunks:
            return f"""Pergunta: {query}

Responda: Desculpe, não encontrei nenhum documento relevante para responder essa pergunta."""

        context_text = "\n\n".join([
            f"[Trecho {i+1} - Documento: {chunk.document_name}]\n{chunk.chunk_text}"
            for i, chunk in enumerate(context_chunks)
        ])

        prompt = f"""Você é um assistente inteligente que responde perguntas baseado em documentos fornecidos.

CONTEXTO DOS DOCUMENTOS:
{context_text}

PERGUNTA DO USUÁRIO: {query}

INSTRUÇÕES:
1. Analise cuidadosamente os trechos dos documentos fornecidos acima
2. Responda a pergunta usando APENAS as informações presentes no contexto
3. Se a informação não estiver disponível nos documentos, diga claramente que não encontrou
4. Seja detalhado e objetivo na resposta
5. Cite o documento ou trecho quando for relevante

RESPOSTA:"""

        return prompt

    async def _generate_with_openai(
        self,
        query: str,
        context_chunks: List[SearchResult]
    ) -> str:
        """
        🔧 VOCÊ INTEGRA: Implementação com OpenAI API

        PASSOS PARA INTEGRAR:
        1. Instalar: pip install openai
        2. Configurar no .env: OPENAI_API_KEY=sk-your-key-here
        3. Adicionar ao config.py: OPENAI_MODEL (opcional, default: gpt-4-turbo-preview)

        EXEMPLO DE IMPLEMENTAÇÃO:
        ```python
        import openai

        prompt = self._build_prompt(query, context_chunks)

        try:
            client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
            response = client.chat.completions.create(
                model=settings.OPENAI_MODEL or "gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": "Você é um assistente inteligente que responde perguntas baseado em documentos."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Erro ao chamar OpenAI: {e}")
            return f"Erro ao processar com OpenAI: {str(e)}"
        ```

        DOCUMENTAÇÃO: https://platform.openai.com/docs/api-reference
        """
        raise NotImplementedError("🔧 VOCÊ INTEGRA: Configure OPENAI_API_KEY no .env e implemente este método seguindo o exemplo acima")

    async def _generate_with_azure(
        self,
        query: str,
        context_chunks: List[SearchResult]
    ) -> str:
        """
        🔧 VOCÊ INTEGRA: Implementação com Azure OpenAI

        PASSOS PARA INTEGRAR:
        1. Instalar: pip install openai
        2. Configurar no .env:
           - AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com/
           - AZURE_OPENAI_API_KEY=your-azure-key
           - AZURE_OPENAI_DEPLOYMENT=gpt-4 (nome do seu deployment)

        EXEMPLO DE IMPLEMENTAÇÃO:
        ```python
        from openai import AzureOpenAI

        prompt = self._build_prompt(query, context_chunks)

        try:
            client = AzureOpenAI(
                api_key=settings.AZURE_OPENAI_API_KEY,
                api_version="2024-02-15-preview",
                azure_endpoint=settings.AZURE_OPENAI_ENDPOINT
            )

            response = client.chat.completions.create(
                model=settings.AZURE_OPENAI_DEPLOYMENT,  # Nome do deployment no Azure
                messages=[
                    {"role": "system", "content": "Você é um assistente inteligente que responde perguntas baseado em documentos."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Erro ao chamar Azure OpenAI: {e}")
            return f"Erro ao processar com Azure OpenAI: {str(e)}"
        ```

        DOCUMENTAÇÃO: https://learn.microsoft.com/azure/ai-services/openai/
        """
        raise NotImplementedError("🔧 VOCÊ INTEGRA: Configure as variáveis AZURE_OPENAI_* no .env e implemente este método seguindo o exemplo acima")

    async def _generate_with_ollama(
        self,
        query: str,
        context_chunks: List[SearchResult]
    ) -> str:
        """Implementação com Ollama"""
        try:
            prompt = self._build_prompt(query, context_chunks)

            ollama_url = f"{settings.OLLAMA_BASE_URL}/api/generate"
            logger.info(f"Tentando conectar ao Ollama em: {ollama_url}")
            logger.info(f"Modelo: {settings.OLLAMA_MODEL}")
            logger.debug(f"Prompt completo: {prompt[:500]}...")  # Log dos primeiros 500 chars

            async with httpx.AsyncClient(timeout=120.0) as client:  # Aumentado timeout
                response = await client.post(
                    ollama_url,
                    json={
                        "model": settings.OLLAMA_MODEL,
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "temperature": 0.7,
                            "top_p": 0.9,
                            "top_k": 40
                        }
                    }
                )
                response.raise_for_status()
                result = response.json()
                answer = result.get("response", "Erro ao gerar resposta")

                logger.info(f"Resposta recebida do Ollama: {answer[:200]}...")
                return answer

        except httpx.ConnectError as e:
            logger.error(f"Erro de conexao com Ollama: {e}")
            logger.error(f"URL tentada: {settings.OLLAMA_BASE_URL}")
            return f"❌ Erro de conexao com Ollama em {settings.OLLAMA_BASE_URL}: {str(e)}"
        except httpx.HTTPError as e:
            logger.error(f"Erro HTTP ao chamar Ollama: {e}")
            return f"❌ Erro HTTP ao conectar com Ollama: {str(e)}"
        except Exception as e:
            logger.error(f"Erro inesperado no Ollama: {e}")
            logger.exception("Stack trace completo:")
            return f"❌ Erro inesperado: {str(e)}"

    def _fallback_answer(self, context_chunks: List[SearchResult]) -> str:
        """Resposta fallback quando LLM não está configurado"""
        if not context_chunks:
            return "Nenhum contexto relevante encontrado nos documentos."

        return (
            "🔧 LLM não configurado. Aqui estão os trechos mais relevantes:\n\n" +
            "\n\n---\n\n".join([
                f"📄 {chunk.document_name}\n{chunk.chunk_text[:200]}..."
                for chunk in context_chunks[:3]
            ])
        )
