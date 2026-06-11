import shutil
import tempfile
from configparser import ConfigParser
from pathlib import Path
from typing import Annotated

from fastapi import BackgroundTasks, FastAPI, File, UploadFile
from starlette.responses import FileResponse

from scrapenfill.core.process import Process

app = FastAPI()


@app.post("/convert/")
async def generate_document(source: Annotated[UploadFile, File()]):
    if source.filename is None:
        raise ValueError("No filename supplied")

    config: ConfigParser = ConfigParser()
    config.read("core/config.ini")
    process = Process(config)

    temp_dir = tempfile.mkdtemp()

    file_path = Path(temp_dir) / source.filename
    with open(file_path, "wb") as temp_file:
        temp_file.write(await source.read())

    cv_text = process.extract_text(file_path)
    if not cv_text.strip():
        print("⚠️ Geen tekst gevonden")

    data = process.cv_to_json(cv_text)

    output_path = Path(temp_dir) / f"{Path(source.filename).stem}.docx"
    process.save_docx(data, config["TEMPLATE"]["template"], output_path)

    background_tasks = BackgroundTasks()
    background_tasks.add_task(shutil.rmtree, temp_dir)

    return FileResponse(
        output_path,
        filename=output_path.name,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        background=background_tasks,
    )
