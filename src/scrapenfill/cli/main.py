# Copyright (c) 2026 Leo
# Licensed under the ScrapeNFill Community License

import asyncio
from pathlib import Path

from ..core.process import Process


async def run_process(input_dir, output_dir, template, cv, max_concurrent):
    try:
        Path(output_dir).mkdir(exist_ok=True)

        files = [f for f in Path(input_dir).iterdir() if f.is_file()]
        if not files:
            print("⚠️ Geen bestanden gevonden")
            return

        sem = asyncio.Semaphore(max_concurrent)

        async def process_one(file):
            async with sem:
                print(f"➡️ Processing {file.name}")

                cv_text = cv.extract_text(file)
                if not cv_text.strip():
                    print(f"⚠️ Geen tekst in {file.name}")
                    return

                data = await cv.cv_to_json(cv_text)
                if not data:
                    print(f"⚠️ Geen data geëxtraheerd uit {file.name}")
                    return

                output_path = Path(output_dir) / f"{file.stem}.docx"
                cv.save_docx(data, template, output_path)

                print(f"✅ Saved: {output_path}")

        results = await asyncio.gather(*(process_one(f) for f in files), return_exceptions=True)

        for r in results:
            if isinstance(r, Exception):
                print(f"FOUT: {r}")

    except Exception as e:
        print(f"FOUT: {e}")


def run(config, args):
    input_dir = args.input if args.input else config["DIRECTORIES"]["input"]
    output_dir = args.output if args.output else config["DIRECTORIES"]["output"]
    template = args.template if args.template else config["TEMPLATE"]["template"]
    max_concurrent = int(config.get("PROCESSING", "max_concurrent", fallback="5"))
    cv = Process(config)

    asyncio.run(run_process(input_dir, output_dir, template, cv, max_concurrent))
