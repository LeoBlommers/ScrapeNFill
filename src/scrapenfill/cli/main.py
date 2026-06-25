# Copyright (c) 2026 Leo
# Licensed under the ScrapeNFill Community License

import asyncio

from scrapenfill.core.process import Process


def run(config, args):
    input_dir = args.input if args.input else config["DIRECTORIES"]["input"]
    output_dir = args.output if args.output else config["DIRECTORIES"]["output"]
    template = args.template if args.template else config["TEMPLATE"]["template"]
    max_concurrent = int(config.get("PROCESSING", "max_concurrent", fallback="5"))
    cv = Process(config)

    asyncio.run(cv.process_all(input_dir, output_dir, template, max_concurrent, log=print))
