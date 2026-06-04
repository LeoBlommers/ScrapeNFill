
from pathlib import Path

from core.cv import Cv


def run_process(input_dir, output_dir, template, cv):
    try:
        Path(output_dir).mkdir(exist_ok=True)

        for file in Path(input_dir).iterdir():
            if not file.is_file():
                continue

            print(f"➡️ Processing {file.name}")

            cv_text = cv.extract_text(file)
            if not cv_text.strip():
                print("⚠️ Geen tekst gevonden")
                continue

            data = cv.cv_to_json(cv_text)
            if not data:
                continue

            output_path = Path(output_dir) / f"{file.stem}.docx"
            cv.save_docx(data, template, output_path)

            print(f"✅ Saved: {output_path}")

    except Exception as e:
        print(f"FOUT: {e}")


def run(config, args):
    input_dir = args.input if args.input else config["DIRECTORIES"]["input"]
    output_dir = args.output if args.output else config["DIRECTORIES"]["output"]
    template = args.template if args.template else config["TEMPLATE"]["template"]
    cv = Cv(config)

    run_process(input_dir, output_dir, template, cv)