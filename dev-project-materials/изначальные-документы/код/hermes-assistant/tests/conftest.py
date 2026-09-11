import os
import sys
from pathlib import Path

# тесты гоняем только офлайн — без МодельАПИ и helpdesk
os.environ["LLM_MODE"] = "offline"
os.environ["HELPDESK_MODE"] = "offline"

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
