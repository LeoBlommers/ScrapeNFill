# Copyright (c) 2026 Leo
# Licensed under the ScrapeNFill Community License
import json
from configparser import ConfigParser
from typing import Any

import google.genai as genai
from google.genai import types

from .AIClient import AIClient


class GeminiClient(AIClient):
    def __init__(self, config: ConfigParser):
        self.model = config["GEMINI"]["model"]
        self.client = genai.Client(api_key=config["GEMINI"]["api_key"])

    def extract(self, prompt: str, schema: dict[str, Any]) -> dict[str, Any]:
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=schema["json_schema"]["schema"],
                temperature=0.2,
            ),
        )

        if not response.text:
            raise Exception("No response from Gemini")
        return json.loads(response.text)
