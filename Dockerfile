FROM mcr.microsoft.com/windows/nanoserver:ltsc2025

# uv installeren
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

WORKDIR /app

# Eerst dependency files kopiëren voor caching
COPY pyproject.toml uv.lock ./

# dependencies installeren
RUN uv sync

# rest van project
COPY . .

# build
RUN uv run pyinstaller --onefile src/scrapenfill/main.py