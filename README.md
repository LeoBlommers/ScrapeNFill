![CI](https://github.com/LeoBlommers/ScrapeNFill/actions/workflows/ci.yml/badge.svg)

## License

ScrapeNFill is released under the ScrapeNFill Community License 1.0.

✅ Personal use  
✅ Educational use  
✅ Research use  
✅ Modification and redistribution  

❌ Commercial use without permission

For commercial licensing, contact: info@lbit.nl

# Set up the project

## set up
Install uv

uv sync


## Config
| Section     | Property | Description      | Example                                                       |
|-------------|----------|------------------|---------------------------------------------------------------|
| DIRECTORIES | INPUT    | Input directory  | /path/to/input                                                |
| DIRECTORIES | OUTPUT   | Output directory | /path/to/output                                               |
| TEMPLATE    | template | Template file    | /path/to/template                                             |
| LLM         | provider | LLM provider     | supported providers: CHATGPT, MISTRAL, GEMINI, OLLAMA, CLAUDE |
| CHATGPT     | model    | LLM model        | gpt-5.4-mini                                                  |
| CHATGPT     | api_key  | API key          |                                                               |
| MISTRAL     | model    | LLM model        | mistral-small                                                 |
| MISTRAL     | api_key  | API key          |                                                               |
| GEMINI      | model    | LLM model        | gemini-pro                                                    |
| GEMINI      | api_key  | API key          |                                                               |
| OLLAMA      | model    | LLM model        | qwen3:32b                                                     |
| CLAUDE      | model    | LLM model        | claude-sonnet-4-20250514                                      |
| CLAUDE      | api_key  | API key          |                                                               |
| PROCESSING  | max_concurrent | Max parallel LLM calls | 5                                                      |

## Define a model

Example:
```json
{
  "type": "json_schema",
  "json_schema": {
    "name": "cv_data",
    "schema": {
      "type": "object",
      "properties": {
        "voornaam": {
          "type": "string"
        }
      }
    }
  }
}
```

## Define an output template

{{ voornaam }}

{{ werkervaring[0].bedrijf}}

{% for expertise in architectuur_en_domeinen_expertise %}
•	{{ expertise }}{% endfor %}

See https://docxtpl.readthedocs.io/en/latest/

# Lint your code
uv run ruff check .

# Auto-fix issues where possible
uv run ruff check --fix .

# Format your code
uv run ruff format .

# type check your code
uv run pyright

# Run

Run CLI (from src/):
python -m scrapenfill.scrapenfill --mode cli

Run desktop GUI (from src/):
python -m scrapenfill.scrapenfill --mode desktop

Start REST API (from src/):
uv run fastapi dev scrapenfill.rest.app

# Build executable
uv run pyinstaller \
  --onefile \
  src/scrapenfill/scrapenfill.py

Build via Docker
docker build -t formatcvs-win .


# Ollama

Install ollama from https://ollama.com/download/mac?utm_source=chatgpt.com

Start ollama server: ollama serve
ollama ps
ollama run qwen3:32b