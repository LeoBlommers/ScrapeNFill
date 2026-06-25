import sys
from pathlib import Path

if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent.parent))

from scrapenfill import scrap_n_fill

scrap_n_fill()
