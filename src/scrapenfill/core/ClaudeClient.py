# Copyright (c) 2026 Leo
# Licensed under the ScrapeNFill Community License

import json
from configparser import ConfigParser
from typing import Any

from anthropic import AsyncAnthropic

from .AIClient import AIClient


class ClaudeClient(AIClient):
    def __init__(self, config: ConfigParser):
        self.model = config["CLAUDE"]["model"]
        self.client = AsyncAnthropic(api_key=config["CLAUDE"]["api_key"])

    async def extract(self, prompt: str, schema: dict[str, Any]) -> dict[str, Any]:
        response = await self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            tools=[
                {
                    "name": "scrappeNFill",
                    "description": "Extract information",
                    "input_schema": schema["json_schema"]["schema"],
                }
            ],
            tool_choice={"type": "tool", "name": "scrappeNFill"},
            messages=[{"role": "user", "content": prompt}],
        )

        if not response.content:
            raise Exception("No response from Claude")
        assert isinstance(response.content[0], str)
        return json.loads(response.content[0])
