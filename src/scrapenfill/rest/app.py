from configparser import ConfigParser
from pathlib import Path
from tempfile import TemporaryDirectory

from anyio.streams import file
from fastapi import UploadFile, File, FastAPI
from starlette.responses import FileResponse

from scrapenfill.core.process import Process

app = FastAPI()

@app.post("/convert/")
async def generate_document(source: UploadFile = File(...)):
    print(source.filename)
    config: ConfigParser = ConfigParser()
    config.read("src/scrapenfill/config.ini")
    process = Process(config)

    with (TemporaryDirectory() as temp_dir):
        file_path = Path(temp_dir) / source.filename
        with open(file_path, "wb") as temp_file:
            temp_file.write(await source.read())

        cv_text = process.extract_text(file_path)
        if not cv_text.strip():
            print("⚠️ Geen tekst gevonden")

        data = process.cv_to_json(cv_text)

        output_path = Path(temp_dir) / f"{file.stem}.docx"
        process.save_docx(data, config["TEMPLATE"]["template"], output_path)

        return FileResponse(
            output_path,
            filename=f"{file.stem}.docx",
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

