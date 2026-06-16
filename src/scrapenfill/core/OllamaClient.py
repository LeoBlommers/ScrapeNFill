# Copyright (c) 2026 Leo
# Licensed under the ScrapeNFill Community License

import json
from configparser import ConfigParser
from typing import Any

from ollama import chat

from .AIClient import AIClient


class OllamaClient(AIClient):
    def __init__(self, config: ConfigParser):
        self.model = config["OLLAMA"]["model"]

    def extract(self, prompt: str, schema: dict[str, Any]) -> dict[str, Any]:
        response = chat(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            format=schema["json_schema"]["schema"],
        )

        if not response.message or not response.message.content:
            raise Exception("No response from Ollama")
        assert isinstance(response.message.content, str)
        content: str = response.message.content
        return json.loads(content)
