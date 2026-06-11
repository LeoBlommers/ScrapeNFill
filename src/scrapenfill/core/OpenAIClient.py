# Copyright (c) 2026 Leo
# Licensed under the ScrapeNFill Community License

import json
from configparser import ConfigParser
from typing import Any, cast

from openai import OpenAI
from openai.types.shared_params.response_format_json_schema import ResponseFormatJSONSchema

from .AIClient import AIClient


class OpenAIClient(AIClient):
    def __init__(self, config: ConfigParser):
        self.client = OpenAI(api_key=config["CHATGPT"]["api_key"])
        self.model = config["CHATGPT"]["model"]

    def extract(self, prompt: str, schema: dict[str, Any]) -> dict[str, Any]:

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            response_format=cast(ResponseFormatJSONSchema, schema),
        )

        if not response.choices or not response.choices[0].message.content:
            raise Exception("No response from OpenAI")
        content: str = response.choices[0].message.content
        return json.loads(content)
