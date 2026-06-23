# Copyright (c) 2026 Leo
# Licensed under the ScrapeNFill Community License

import json
from configparser import ConfigParser
from typing import Any, cast

from openai import AsyncOpenAI

from .AIClient import AIClient


class OpenAIClient(AIClient):
    def __init__(self, config: ConfigParser):
        self.client = AsyncOpenAI(api_key=config["CHATGPT"]["api_key"])
        self.model = config["CHATGPT"]["model"]

    async def extract(self, prompt: str, schema: dict[str, Any]) -> dict[str, Any]:
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            response_format=cast(Any, schema),
        )

        if not response.choices or not response.choices[0].message.content:
            raise Exception("No response from OpenAI")
        content: str = response.choices[0].message.content
        return json.loads(content)
