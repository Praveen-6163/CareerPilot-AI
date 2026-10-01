import os
from PyPDF2 import PdfReader
from docx import Document

ALLOWED_EXTENSIONS = {'.pdf', '.docx', '.txt'}


def extract_text_from_file(file_path, filename):
    ext = os.path.splitext(filename)[1].lower()

    if ext == '.pdf':
        try:
            reader = PdfReader(file_path)
            text_blocks = []
            for page in reader.pages:
                page_text = page.extract_text() or ''
                text_blocks.append(page_text)
            return '\n'.join(text_blocks)
        except Exception as exc:
            raise ValueError(f'PDF extraction failed: {exc}')

    if ext == '.docx':
        try:
            doc = Document(file_path)
            paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
            return '\n'.join(paragraphs)
        except Exception as exc:
            raise ValueError(f'DOCX extraction failed: {exc}')

    if ext == '.txt':
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        except Exception as exc:
            raise ValueError(f'TXT extraction failed: {exc}')

    raise ValueError('Unsupported file format.')
