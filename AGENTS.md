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
├── __main__.py            # python -m scrapenfill entrypoint
├── scrapenfill.py         # Entrypoint (--mode cli|desktop)
├── cli/main.py            # CLI mode (delegates to Process.process_all)
├── desktop/main.py        # tkinter GUI mode (delegates to Process.process_all)
├── rest/app.py            # FastAPI server
└── core/
    ├── process.py         # Process class (text extraction, LLM call, docx rendering, batch process_all)
    ├── AIClient.py        # ABC base (async def extract)
    ├── {OpenAI,Claude,Gemini,Mistral,Ollama}Client.py
    ├── model              # JSON schema for CV (NO extension)
    └── prompt             # Dutch LLM system prompt (NO extension)
```

## Quirks & gotchas

- `core/model` and `core/prompt` have **no file extension** — opened via `Path(__file__).parent / "model"` derived from package location.
- `core/config.ini` is gitignored (contains API keys). Copy from `config.ini.example`. Paths to it now use `_PKG_DIR` / `_CORE_DIR` constants.
- `core/config.ini` is gitignored (contains API keys). Copy from `config.ini.example`.
- `.spec` files under repo root reference old `src/formatcvs/` paths — they are stale. Use the inline `pyinstaller` command above.
- Dockerfile CMD is stale (references `/app/main.py`). Real REST entrypoint: `src/scrapenfill/rest/app.py`.
- Tests in `tests/`: `test_process.py` (Process class), `test_ai_clients.py` (all 5 AI clients), `test_api.py` (FastAPI routing). Run with `uv run pytest`.
- Git track: CI runs on `main` + `develop` + PRs. Releases on tags `v*` build a Windows `.exe`.
