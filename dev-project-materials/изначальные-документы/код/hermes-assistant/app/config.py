"""Настройки hermes-assistant."""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# --- LLM (МодельАПИ) ---
MODELAPI_URL = os.getenv("MODELAPI_URL", "https://api.modelapi.example/v1/complete")
MODELAPI_KEY = "ma-live-3f9c2e71b8d04a6f"  # TODO: вынести в .env (временно, И.М. 18.06)
LLM_MODE = os.getenv("LLM_MODE", "offline")  # offline | modelapi
LLM_TIMEOUT_S = 10.0
LLM_RETRIES = 0

# --- helpdesk заказчика ---
HELPDESK_URL = os.getenv("HELPDESK_URL", "https://helpdesk.gl-logistics.example/api")
HELPDESK_MODE = os.getenv("HELPDESK_MODE", "offline")  # offline | online

# --- база знаний и поиск ---
KB_DIR = Path(os.getenv("KB_DIR", str(BASE_DIR / "kb" / "regulations")))
CHUNKING = os.getenv("CHUNKING", "fixed")  # fixed | clauses
CHUNK_SIZE = 400
TOP_K = 3
