# Copyright (c) 2026 Leo
# Licensed under the ScrapeNFill Community License

import asyncio
import json
from collections.abc import Iterator
from configparser import ConfigParser
from pathlib import Path
from typing import cast

import pdfplumber
from docx import Document
from docx.document import Document as DocumentType
from docx.table import Table
from docx.text.paragraph import Paragraph
from docxtpl import DocxTemplate

from .ClaudeClient import ClaudeClient
from .GeminiClient import GeminiClient
from .MistralClient import MistralClient
from .OllamaClient import OllamaClient
from .OpenAIClient import OpenAIClient

_PKG_DIR = Path(__file__).parent.resolve()


class Process:
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
    async def cv_to_json(self, input_text):
        with open(_PKG_DIR / "model") as file:
            format = json.load(file)
        with open(_PKG_DIR / "prompt") as file:
            prompt = file.read()

        prompt = f"""
            {prompt}
            
            Input:
            \"\"\"
            {input_text}
            \"\"\"
            """

        match self.config["LLM"]["provider"]:
            case "CHATGPT":
                client = OpenAIClient(config=self.config)
            case "MISTRAL":
                client = MistralClient(config=self.config)
            case "GEMINI":
                client = GeminiClient(config=self.config)
            case "OLLAMA":
                client = OllamaClient(config=self.config)
            case "CLAUDE":
                client = ClaudeClient(config=self.config)
            case _:
                raise Exception("Invalid LLM provider")

        return await client.extract(prompt, format)

    # =========================
    # BATCH PROCESSING
    # =========================
    async def process_all(self, input_dir, output_dir, template, max_concurrent=5, log=None):
        log = log or (lambda msg: None)

        Path(output_dir).mkdir(exist_ok=True)

        files = [f for f in Path(input_dir).iterdir() if f.is_file()]
        if not files:
            log("⚠️ Geen bestanden gevonden")
            return

        sem = asyncio.Semaphore(max_concurrent)

        async def process_one(file):
            async with sem:
                log(f"➡️ Processing {file.name}")

                cv_text = self.extract_text(file)
                if not cv_text.strip():
                    log(f"⚠️ Geen tekst in {file.name}")
                    return

                data = await self.cv_to_json(cv_text)
                if not data:
                    log(f"⚠️ Geen data geëxtraheerd uit {file.name}")
                    return

                output_path = Path(output_dir) / f"{file.stem}.docx"
                self.save_docx(data, template, output_path)

                log(f"✅ Saved: {output_path}")

        results = await asyncio.gather(*(process_one(f) for f in files), return_exceptions=True)

        for r in results:
            if isinstance(r, Exception):
                log(f"FOUT: {r}")

    # =========================
    # OUTPUT
    # =========================
    def save_docx(self, data, template, path):
        doc = DocxTemplate(template)
        doc.render(data)
        doc.save(path)
