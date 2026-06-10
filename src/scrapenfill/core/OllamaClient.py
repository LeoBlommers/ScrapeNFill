# Copyright (c) 2026 Leo
# Licensed under the ScrapeNFill Community License

import json
from configparser import ConfigParser
from typing import Any

from core.AIClient import AIClient
from ollama import chat


class MistralClient(AIClient):
    def __init__(self, config: ConfigParser):
        self.model = config["MISTRAL"]["model"]

    def extract(self, prompt: str, schema: dict[str, Any]) -> dict[str, Any]:
        response = chat(
            model="qwen3:14b",
            messages=[{"role": "user", "content": prompt}],
            format=schema,
        )

        if not response.message or not response.message.content:
            raise Exception("No response from OpenAI")
        assert isinstance(response.message.content, str)
        content: str = response.message.content
        return json.loads(content)
