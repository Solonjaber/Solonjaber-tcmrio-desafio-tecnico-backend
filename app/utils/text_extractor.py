import PyPDF2
from docx import Document as DocxDocument
from typing import Tuple
import os

class TextExtractor:
    """
    Extrai texto de documentos PDF e DOCX

    Responsabilidades:
    - Extrair texto de PDF
    - Extrair texto de DOCX
    - Contar páginas/palavras
    """

    @staticmethod
    def extract_from_pdf(file_path: str) -> Tuple[str, int]:
        """
        Extrai texto de PDF
        Retorna: (texto_completo, número_de_páginas)
        """
        text_content = []

        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            page_count = len(pdf_reader.pages)

            for page in pdf_reader.pages:
                text = page.extract_text()
                if text:
                    text_content.append(text)

        full_text = "\n\n".join(text_content)
        return full_text, page_count

    @staticmethod
    def extract_from_docx(file_path: str) -> Tuple[str, int]:
        """
        Extrai texto de DOCX
        Retorna: (texto_completo, número_de_parágrafos)
        """
        doc = DocxDocument(file_path)

        paragraphs = []
        for para in doc.paragraphs:
            if para.text.strip():
                paragraphs.append(para.text)

        full_text = "\n\n".join(paragraphs)
        return full_text, len(paragraphs)

    @staticmethod
    def count_words(text: str) -> int:
        """Conta palavras no texto"""
        return len(text.split())

    @staticmethod
    def extract_text(file_path: str, file_type: str) -> Tuple[str, int, int]:
        """
        Extrai texto baseado no tipo de arquivo
        Retorna: (texto, páginas/parágrafos, palavras)
        """
        if file_type == "pdf":
            text, page_count = TextExtractor.extract_from_pdf(file_path)
        elif file_type == "docx":
            text, page_count = TextExtractor.extract_from_docx(file_path)
        else:
            raise ValueError(f"Tipo de arquivo não suportado: {file_type}")

        word_count = TextExtractor.count_words(text)
        return text, page_count, word_count
