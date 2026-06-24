from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from scrapenfill.core.ClaudeClient import ClaudeClient
from scrapenfill.core.GeminiClient import GeminiClient
from scrapenfill.core.MistralClient import MistralClient
from scrapenfill.core.OllamaClient import OllamaClient
from scrapenfill.core.OpenAIClient import OpenAIClient

SAMPLE_SCHEMA = {
    "json_schema": {
        "schema": {
            "type": "object",
            "properties": {
                "voornaam": {"type": "string"},
                "achternaam": {"type": "string"},
            },
        }
    }
}


async def test_openai_client_extract(config):
    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(message=MagicMock(content='{"voornaam": "Jan", "achternaam": "Jansen"}'))
    ]
    mock_client = AsyncMock()
    mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

    with patch("scrapenfill.core.OpenAIClient.AsyncOpenAI", return_value=mock_client):
        client = OpenAIClient(config)
        result = await client.extract("test prompt", SAMPLE_SCHEMA)

    assert result == {"voornaam": "Jan", "achternaam": "Jansen"}
    mock_client.chat.completions.create.assert_awaited_once()


async def test_openai_client_empty_response_raises(config):
    mock_response = MagicMock()
    mock_response.choices = []
    mock_client = AsyncMock()
    mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

    with patch("scrapenfill.core.OpenAIClient.AsyncOpenAI", return_value=mock_client):
        client = OpenAIClient(config)
        with pytest.raises(Exception, match="No response from OpenAI"):
            await client.extract("test prompt", SAMPLE_SCHEMA)


async def test_claude_client_extract(config):
    mock_response = MagicMock()
    mock_response.content = ['{"voornaam": "Jan", "achternaam": "Jansen"}']
    mock_client = AsyncMock()
    mock_client.messages.create = AsyncMock(return_value=mock_response)

    with patch("scrapenfill.core.ClaudeClient.AsyncAnthropic", return_value=mock_client):
        client = ClaudeClient(config)
        result = await client.extract("test prompt", SAMPLE_SCHEMA)

    assert result == {"voornaam": "Jan", "achternaam": "Jansen"}
    mock_client.messages.create.assert_awaited_once()


async def test_claude_client_empty_response_raises(config):
    mock_response = MagicMock()
    mock_response.content = []
    mock_client = AsyncMock()
    mock_client.messages.create = AsyncMock(return_value=mock_response)

    with patch("scrapenfill.core.ClaudeClient.AsyncAnthropic", return_value=mock_client):
        client = ClaudeClient(config)
        with pytest.raises(Exception, match="No response from Claude"):
            await client.extract("test prompt", SAMPLE_SCHEMA)


async def test_gemini_client_extract(config):
    mock_response = MagicMock()
    mock_response.text = '{"voornaam": "Jan", "achternaam": "Jansen"}'
    mock_client = AsyncMock()
    mock_client.aio.models.generate_content = AsyncMock(return_value=mock_response)

    with patch("scrapenfill.core.GeminiClient.genai.Client", return_value=mock_client):
        client = GeminiClient(config)
        result = await client.extract("test prompt", SAMPLE_SCHEMA)

    assert result == {"voornaam": "Jan", "achternaam": "Jansen"}
    mock_client.aio.models.generate_content.assert_awaited_once()


async def test_gemini_client_empty_response_raises(config):
    mock_response = MagicMock()
    mock_response.text = None
    mock_client = AsyncMock()
    mock_client.aio.models.generate_content = AsyncMock(return_value=mock_response)

    with patch("scrapenfill.core.GeminiClient.genai.Client", return_value=mock_client):
        client = GeminiClient(config)
        with pytest.raises(Exception, match="No response from Gemini"):
            await client.extract("test prompt", SAMPLE_SCHEMA)


async def test_mistral_client_extract(config):
    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(message=MagicMock(content='{"voornaam": "Jan", "achternaam": "Jansen"}'))
    ]
    mock_client = MagicMock()
    mock_client.chat.complete_async = AsyncMock(return_value=mock_response)

    with patch("scrapenfill.core.MistralClient.Mistral", return_value=mock_client):
        client = MistralClient(config)
        result = await client.extract("test prompt", SAMPLE_SCHEMA)

    assert result == {"voornaam": "Jan", "achternaam": "Jansen"}
    mock_client.chat.complete_async.assert_awaited_once()


async def test_mistral_client_empty_response_raises(config):
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content=None))]
    mock_client = MagicMock()
    mock_client.chat.complete_async = AsyncMock(return_value=mock_response)

    with patch("scrapenfill.core.MistralClient.Mistral", return_value=mock_client):
        client = MistralClient(config)
        with pytest.raises(Exception, match="No response from Mistral"):
            await client.extract("test prompt", SAMPLE_SCHEMA)


async def test_ollama_client_extract(config):
    mock_response = MagicMock()
    mock_response.message.content = '{"voornaam": "Jan", "achternaam": "Jansen"}'
    mock_client = AsyncMock()
    mock_client.chat = AsyncMock(return_value=mock_response)

    with patch("scrapenfill.core.OllamaClient.ollama.AsyncClient", return_value=mock_client):
        client = OllamaClient(config)
        result = await client.extract("test prompt", SAMPLE_SCHEMA)

    assert result == {"voornaam": "Jan", "achternaam": "Jansen"}
    mock_client.chat.assert_awaited_once()


async def test_ollama_client_empty_response_raises(config):
    mock_response = MagicMock()
    mock_response.message = None
    mock_client = AsyncMock()
    mock_client.chat = AsyncMock(return_value=mock_response)

    with patch("scrapenfill.core.OllamaClient.ollama.AsyncClient", return_value=mock_client):
        client = OllamaClient(config)
        with pytest.raises(Exception, match="No response from Ollama"):
            await client.extract("test prompt", SAMPLE_SCHEMA)
