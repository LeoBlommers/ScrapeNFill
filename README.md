![CI](https://github.com/LeoBlommers/ScrapeNFill/actions/workflows/ci.yml/badge.svg)

## License

ScrapeNFill is released under the ScrapeNFill Community License 1.0.

✅ Personal use  
✅ Educational use  
✅ Research use  
✅ Modification and redistribution  

❌ Commercial use without permission

For commercial licensing, contact: info@lbit.nl

# Lint your code
uv run ruff check .

# Auto-fix issues where possible
uv run ruff check --fix .

# Format your code
uv run ruff format .

# type check your code
uv run pyright

# Build executable
Build local executable
uv run pyinstaller \
  --onefile \
  src/formatcvs/formatcv.py

Build via Docker
docker build -t formatcvs-win .

docker run --rm -v "$(pwd):/formatcvs" formatcvs-win

# Ollama

Install ollama from https://ollama.com/download/mac?utm_source=chatgpt.com

Start ollama server: ollama serve
ollama ps
ollama run qwen3:32b
