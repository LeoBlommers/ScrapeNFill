import json

from typing import cast
from docx import Document
from docx.document import Document as DocumentType

import pdfplumber
from docxtpl import DocxTemplate
from openai import OpenAI


class Cv:
    def __init__(self, config: dict):
        self.config = config
        self.client = OpenAI(api_key=config["api_key"])

    # =========================
    # TEXT EXTRACTION
    # =========================
    def extract_text_from_pdf(self, path):
        text = ""
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text

    def iter_block_items(self, parent):
        from docx.table import Table
        from docx.text.paragraph import Paragraph

        for child in parent.element.body.iterchildren():
            if child.tag.endswith("p"):
                yield Paragraph(child, parent)
            elif child.tag.endswith("tbl"):
                yield Table(child, parent)

    def extract_text_from_docx(self, path):
        doc: DocumentType = cast(DocumentType, Document(path.as_posix()))
        text = list()
        for block in self.iter_block_items(doc):
            if hasattr(block, "text"):
                text.append(block.text)
            else:
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
            model=self.config["model"],
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            response_format=model
        )

        content: str = resp.choices[0].message.content
#        content = content.replace("```json", "").replace("```", "")
        return json.loads(content)
        try:
            return json.loads(content)
        except Exception:
            print("⚠️ JSON parse error:")
            print(content)
            return None

    # =========================
    # OUTPUT
    # =========================
    def save_docx(self, data, template, path):
        doc = DocxTemplate(template)
        doc.render(data)
        doc.save(path)
