# Copyright (c) 2026 Leo
# Licensed under the ScrapeNFill Community License
from abc import ABC, abstractmethod

class AIClient(ABC):
    @abstractmethod
    async def extract(self, prompt: str, schema: dict) -> dict:
        raise NotImplementedError
