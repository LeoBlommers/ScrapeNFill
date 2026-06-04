class Document:
    paragraphs: list[str]

def load(path: str) -> Document: ...

class Table:
    text: str

class Paragraph:
    row: str
