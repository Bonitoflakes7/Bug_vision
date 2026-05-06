import os

# ── Tesseract OCR ──────────────────────────────────────────────
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# ── Screen capture ─────────────────────────────────────────────
# Coordinates of the terminal/console region you want to watch.
# Run bbox.py to find your coordinates.
CAPTURE_BBOX = (363, 617, 1844, 1041)
CAPTURE_INTERVAL = 5  # seconds between each capture

# ── Ollama / Mistral ───────────────────────────────────────────
OLLAMA_BASE_URL = "http://localhost:11434"
LLM_MODEL = "mistral"
EMBED_MODEL = "nomic-embed-text"  # pulled via: ollama pull nomic-embed-text

# ── RAG / ChromaDB ─────────────────────────────────────────────
# Where ChromaDB stores its index on disk
CHROMA_DB_PATH = os.path.join(os.path.dirname(__file__), "chroma_db")

# How many code chunks to retrieve per error
TOP_K_RESULTS = 4

# ── Screenshots ────────────────────────────────────────────────
SCREENSHOTS_PATH = os.path.join(os.path.dirname(__file__), "screenshots")