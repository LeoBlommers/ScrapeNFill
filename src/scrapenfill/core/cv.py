# Copyright (c) 2026 Leo
# Licensed under the ScrapeNFill Community License

import json
from collections.abc import Iterator
from configparser import ConfigParser
from typing import cast

import pdfplumber
from core.GeminiClient import GeminiClient
from core.MistralClient import MistralClient
from core.OllamaClient import OllamaClient
from core.OpenAIClient import OpenAIClient
from docx import Document
from docx.document import Document as DocumentType
from docx.table import Table
from docx.text.paragraph import Paragraph
from docxtpl import DocxTemplate


class Cv:
    def __init__(self, config: ConfigParser):
        self.config = config

    # =========================
    # TEXT EXTRACTION
    # =========================
    def extract_text_from_pdf(self, path):
        text = ""
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text

    def iter_block_items(self, parent) -> Iterator[Paragraph | Table]:
        from docx.table import Table
        from docx.text.paragraph import Paragraph

        for child in parent.element.body.iterchildren():
            if child.tag.endswith("p"):
                yield Paragraph(child, parent)
            elif child.tag.endswith("tbl"):
                yield Table(child, parent)

    def extract_text_from_docx(self, path):
        doc = cast(DocumentType, Document(str(path)))  # pyright: ignore[reportCallIssue]
        text: list[str] = []

        for block in self.iter_block_items(doc):
            if isinstance(block, Paragraph):
                text.append(block.text)
            elif isinstance(block, Table):
                # tabel
                for row in block.rows:
                    for cell in row.cells:
                        text.append(cell.text)

        return "\n".join(text)

    def extract_text(self, path):
        if path.suffix.lower() == ".pdf":
            return self.extract_text_from_pdf(path)
        elif path.suffix.lower() == ".docx":
            return self.extract_text_from_docx(path)
        elif path.suffix.lower() == ".txt":
            return path.read_text(encoding="utf-8")
        return ""

    # =========================
    # STEP 1: CV → JSON
    # =========================
    def cv_to_json(self, cv_text):
        with open("core/model") as file:
            format = json.load(file)
        with open("core/prompt") as file:
            prompt = file.read()

        prompt = f"""
            {prompt}
            
            CV:
ƒ            \"\"\"
            {cv_text}
            \"\"\"
            """
        if self.config["LLM"]["provider"] == "CHATGPT":
            client = OpenAIClient(config=self.config)
        elif self.config["LLM"]["provider"] == "MISTRAL":
            client = MistralClient(config=self.config)
        elif self.config["LLM"]["provider"] == "GEMINI":
            client = GeminiClient(config=self.config)
        elif self.config["LLM"]["provider"] == "OLLAMA":
            client = OllamaClient(config=self.config)
        else:
            raise Exception("Invalid LLM provider")

        return client.extract(prompt, format)

    # =========================
    # OUTPUT
    # =========================
    def save_docx(self, data, template, path):
        doc = DocxTemplate(template)
        doc.render(data)
        doc.save(path)
