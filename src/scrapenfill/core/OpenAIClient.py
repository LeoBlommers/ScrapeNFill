import json
from configparser import ConfigParser
from typing import Any, cast

from core.AIClient import AIClient
from openai import OpenAI
from openai.types.shared_params.response_format_json_schema import ResponseFormatJSONSchema


class OpenAIClient(AIClient):
    def __init__(self, config: ConfigParser):
        self.client = OpenAI(api_key=config["CHATGPT"]["api_key"])
        self.model = config["CHATGPT"]["model"]

    def extract(self, prompt: str, schema: dict[str, Any]) -> dict[str, Any]:

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            response_format=cast(
                ResponseFormatJSONSchema,
                {
                    "type": "json_schema",
                    "json_schema": {
                        "name": "result",
                        "schema": schema,
                        "strict": True,
                    },
                },
            ),
        )

        if not response.choices or not response.choices[0].message.content:
            raise Exception("No response from OpenAI")
        content: str = response.choices[0].message.content
        return json.loads(content)
