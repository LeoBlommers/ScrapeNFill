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