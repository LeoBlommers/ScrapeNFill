# ScrapeNFill — AGENTS.md

## Toolchain (Python 3.14 via `uv`)

| Action | Command |
|--------|---------|
| Install | `uv sync` |
| Lint | `uv run ruff check .` |
| Format | `uv run ruff format .` |
| Typecheck | `uv run pyright` |
| Test | `uv run pytest` |
| Run CLI | `cd src && python -m scrapenfill.scrapenfill --mode cli` |
| Run GUI | `cd src && python -m scrapenfill.scrapenfill --mode desktop` |
| Start REST API | `cd src && uv run fastapi dev scrapenfill.rest.app` |
| Build CLI exe | `uv run pyinstaller --onefile src/scrapenfill/scrapenfill.py` |

**CI order** (`.github/workflows/ci.yml`): lint → format check → typecheck → test → build.

Ruff: `line-length=100`, `quote-style="double"`, lint `select = ["E4", "E7", "E9", "F", "B", "I", "UP"]`.

## Package structure

```
src/scrapenfill/           # Python package
├── scrapenfill.py         # Entrypoint (--mode cli|desktop)
├── cli/main.py            # CLI mode
├── desktop/main.py        # tkinter GUI mode
├── rest/app.py            # FastAPI server
└── core/
    ├── process.py         # Process class (text extraction, LLM call, docx rendering)
    ├── AIClient.py        # Abstract base
    ├── {OpenAI,Claude,Gemini,Mistral,Ollama}Client.py
    ├── model              # JSON schema for CV (NO extension)
    └── prompt             # Dutch LLM system prompt (NO extension)
```

## Quirks & gotchas

- `core/model` and `core/prompt` have **no file extension** — opened as `"core/model"` and `"core/prompt"` in code.
- `core/config.ini` is gitignored (contains API keys). Copy from `config.ini.example`.
- `.spec` files under repo root reference old `src/formatcvs/` paths — they are stale. Use the inline `pyinstaller` command above.
- Dockerfile CMD is stale (references `/app/main.py`). Real REST entrypoint: `src/scrapenfill/rest/app.py`.
- Only 1 test exists (`tests/test_main.py`, placeholder).
- Git track: CI runs on `main` + `develop` + PRs. Releases on tags `v*` build a Windows `.exe`.
