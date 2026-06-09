import json

from core.AIClient import AIClient
from openai import OpenAI


class OpenAIClient(AIClient):
    def __init__(self, api_key: str, model: str):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def extract(self, prompt: str, format: object) -> object:

        response = self.client.beta.chat.completions.parse(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            response_format=format,
        )

        return json.loads(response.choices[0].message.content)
