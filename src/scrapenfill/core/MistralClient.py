import json
from typing import Any, cast

from core.AIClient import AIClient
from mistralai.client import Mistral


class MistralClient(AIClient):
    def __init__(self, api_key: str, model: str):
        self.client = Mistral(api_key=api_key)
        self.model = model

    def extract(self, prompt: str, schema: dict[str, Any]) -> dict[str, Any]:

        response = self.client.chat.complete(
            model="mistral-large-latest",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            response_format=cast(Any, {
                "type": "json_schema",
                "json_schema": {
                    "name": "result",
                    "schema": schema,
                    "strict": True,
                },
            }
                                 )
        )

        if not response.choices[0].message or not response.choices[0].message.content:
            raise Exception("No response from OpenAI")
        assert isinstance(response.choices[0].message.content, str)
        content: str = response.choices[0].message.content
        return json.loads(content)


