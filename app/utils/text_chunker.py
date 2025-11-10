from typing import List

class TextChunker:
    """
    Divide texto em chunks para vetorização

    Responsabilidades:
    - Dividir texto em pedaços gerenciáveis
    - Manter contexto entre chunks (overlap)
    """

    @staticmethod
    def chunk_text(
        text: str,
        chunk_size: int = 500,
        overlap: int = 50
    ) -> List[str]:
        """
        Divide texto em chunks com overlap

        Args:
            text: Texto para dividir
            chunk_size: Tamanho aproximado de cada chunk em palavras
            overlap: Número de palavras para sobrepor entre chunks
        """
        words = text.split()
        chunks = []

        start = 0
        while start < len(words):
            end = start + chunk_size
            chunk_words = words[start:end]
            chunk_text = " ".join(chunk_words)

            if chunk_text.strip():
                chunks.append(chunk_text)

            start = end - overlap

        return chunks
