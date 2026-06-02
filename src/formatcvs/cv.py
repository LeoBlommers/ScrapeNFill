import json
from configparser import ConfigParser

from typing import cast, Iterator
from docx import Document
from docx.document import Document as DocumentType

import pdfplumber
from docx.table import Table
from docx.text.paragraph import Paragraph
from docxtpl import DocxTemplate
from openai import OpenAI


class Cv:
    def __init__(self, config: ConfigParser):
        self.config = config
        self.client = OpenAI(api_key=config["CHATGPT"]["api_key"])

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
        with open("model") as file:
            model = json.load(file)
        with open("prompt") as file:
            prompt = file.read()

        prompt = f"""
            {prompt}
            
            CV:
            \"\"\"
            {cv_text}
            \"\"\"
            """

        resp = self.client.chat.completions.create(
            model=self.config["CHATGPT"]["model"],
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            response_format=model
        )
        if not resp.choices or not resp.choices[0].message.content:
            raise Exception("No response from OpenAI")
        content: str = resp.choices[0].message.content
        return json.loads(content)


    # =========================
    # OUTPUT
    # =========================
    def save_docx(self, data, template, path):
        doc = DocxTemplate(template)
        doc.render(data)
        doc.save(path)
